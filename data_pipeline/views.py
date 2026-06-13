import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .models import Document

from .services.extractor import extract_text
from .services.cleaner import clean_text
from .services.chunker import chunk_text
from .services.embeddings import generate_embeddings
from .services.vector_store import collection
from .services.search_service import semantic_search
from drf_spectacular.utils import extend_schema
import time
from .serializers import (
    SearchSerializer,
    DocumentSerializer
)
from .services.quality_service import calculate_quality
from django.db.models import Avg, Sum

# Create your views here.


@extend_schema(
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "format": "binary"
                }
            }
        }
    }
)
class UploadDocumentView(APIView):

    parser_classes = [MultiPartParser]

    def post(self, request):

        start_time = time.time()

        if "file" not in request.FILES:
            return Response(
                {"error": "No file provided"},
                status=400
            )

        file = request.FILES["file"]

        text = extract_text(file)

        cleaned_text = clean_text(text)

        chunks = chunk_text(cleaned_text)

        quality_data = calculate_quality(
            chunks
        )

        embeddings = generate_embeddings(chunks)

        processing_time = round(
            time.time() - start_time,
            2
        )

        document = Document.objects.create(
            filename=file.name,
            total_characters=len(cleaned_text),
            total_chunks=len(chunks),
            processing_time=processing_time,
            status="COMPLETED",
            quality_score=quality_data["quality_score"],
            duplicate_chunks=quality_data["duplicate_chunks"]
        )

        for index, chunk in enumerate(chunks):

            collection.add(
                ids=[str(uuid.uuid4())],
                embeddings=[embeddings[index].tolist()],
                documents=[chunk],
                metadatas=[{
                    "document_id": document.id,
                    "chunk": index
                }]
            )

        return Response({
            "message": "Document processed successfully",
            "document_id": document.id,
            "chunks": len(chunks)
        })



@extend_schema(
    request=SearchSerializer,
    responses={200: dict}
)
class SearchView(APIView):

    def post(self, request):

        query = request.data.get("query")

        if not query:
            return Response(
                {"error": "No query provided"},
                status=400
            )

        results = semantic_search(query)

        return Response(results)
    


class DocumentListView(APIView):

    def get(self, request):

        documents = Document.objects.all().order_by(
            "-uploaded_at"
        )

        serializer = DocumentSerializer(
            documents,
            many=True
        )

        return Response(serializer.data)
    

    
class StatsView(APIView):
    def get(self, request):
        documents = Document.objects.count()

        total_chunks = (
            Document.objects.aggregate(
                total=Sum("total_chunks")
            )["total"]
            or 0
        )

        average_quality = (
            Document.objects.aggregate(
                avg=Avg("quality_score")
            )["avg"]
            or 0
        )

        return Response({
            "documents": documents,
            "total_chunks": total_chunks,
            "average_quality": round(average_quality, 2)
        })  