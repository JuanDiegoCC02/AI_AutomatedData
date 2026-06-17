import uuid
import time

from collections import Counter

from django.db.models import Avg, Sum
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from drf_spectacular.utils import extend_schema

from .models import Document

from .serializers import (
    DashboardSerializer,
    QualityReportSerializer,
    SearchSerializer,
    DocumentSerializer,
    StatsSerializer
)

from .services.extractor import extract_text
from .services.cleaner import clean_text
from .services.chunker import chunk_text
from .services.embeddings import generate_embeddings
from .services.vector_store import collection
from .services.search_service import semantic_search
from .services.quality_service import calculate_quality
from .services.language_detector import detect_language
from .services.complexity_service import calculate_complexity


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

        try:

            file_size = file.size

            text = extract_text(file)

            cleaned_text = clean_text(text)

            language = detect_language(
                cleaned_text
            )

            complexity_score = calculate_complexity(
                cleaned_text
            )

            chunks = chunk_text(
                cleaned_text
            )

            quality_data = calculate_quality(
                chunks
            )

            embeddings = generate_embeddings(
                chunks
            )

            processing_time = round(
                time.time() - start_time,
                2
            )

            document = Document.objects.create(
                filename=file.name,
                total_characters=len(cleaned_text),
                total_chunks=len(chunks),
                processing_time=processing_time,
                quality_score=quality_data["quality_score"],
                duplicate_chunks=quality_data["duplicate_chunks"],
                language=language,
                complexity_score=complexity_score,
                status="COMPLETED",
                file_size=file_size,
                processed_at=timezone.now()
            )

            for index, chunk in enumerate(chunks):

                collection.add(
                    ids=[str(uuid.uuid4())],
                    embeddings=[
                        embeddings[index].tolist()
                    ],
                    documents=[chunk],
                    metadatas=[{
                        "document_id": document.id,
                        "chunk": index
                    }]
                )

            return Response({
                "message": "Document processed successfully",
                "document_id": document.id,
                "filename": document.filename,
                "chunks": len(chunks),
                "language": language,
                "quality_score": quality_data["quality_score"]
            })

        except Exception as e:

            Document.objects.create(
                filename=file.name,
                status="FAILED",
                error_message=str(e)
            )

            return Response(
                {
                    "error": str(e)
                },
                status=500
            )


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

        search_results = []

        for i in range(
            len(results["documents"][0])
        ):

            metadata = results["metadatas"][0][i]

            document = Document.objects.get(
                id=metadata["document_id"]
            )

            search_results.append({
                "filename": document.filename,
                "content": results["documents"][0][i],
                "distance": results["distances"][0][i]
            })

        return Response({
            "query": query,
            "results": search_results
        })

 
    


class DocumentListView(APIView):

    def get(self, request):

        documents = Document.objects.all().order_by(
            "-uploaded_at"
        )

        serializer = DocumentSerializer(
            documents,
            many=True
        )

        return Response(
            serializer.data
        )
    


@extend_schema(
    responses=StatsSerializer
)
class StatsView(APIView):

    def get(self, request):

        documents = Document.objects.count()

        total_chunks = (
            Document.objects.aggregate(
                total=Sum("total_chunks")
            )["total"] or 0
        )

        average_quality = (
            Document.objects.aggregate(
                avg=Avg("quality_score")
            )["avg"] or 0
        )

        return Response({
            "documents": documents,
            "total_chunks": total_chunks,
            "average_quality": round(
                average_quality,
                2
            )
        })
    


@extend_schema(
    responses=QualityReportSerializer
)
class QualityReportView(APIView):

    def get(self, request):

        documents = Document.objects.all()

        average_quality = (
            Document.objects.aggregate(
                avg=Avg("quality_score")
            )["avg"] or 0
        )

        total_duplicates = (
            Document.objects.aggregate(
                total=Sum("duplicate_chunks")
            )["total"] or 0
        )

        languages = Counter(
            documents.values_list(
                "language",
                flat=True
            )
        )

        return Response({
            "documents": documents.count(),
            "average_quality": round(
                average_quality,
                2
            ),
            "total_duplicates": total_duplicates,
            "languages": dict(languages)
        })
    

@extend_schema(
    responses=DashboardSerializer
)
class DashboardView(APIView):

    def get(self, request):

        return Response({

            "documents":
            Document.objects.count(),

            "completed":
            Document.objects.filter(
                status="COMPLETED"
            ).count(),

            "failed":
            Document.objects.filter(
                status="FAILED"
            ).count(),

            "languages":
            list(
                Document.objects.values_list(
                    "language",
                    flat=True
                ).distinct()
            )
        })
    


class TopDocumentsView(APIView):

    def get(self, request):

        documents = (
            Document.objects
            .order_by("-quality_score")[:5]
        )

        serializer = DocumentSerializer(
            documents,
            many=True
        )

        return Response(
            serializer.data
        )