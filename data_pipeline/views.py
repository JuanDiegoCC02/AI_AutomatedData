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
from .serializers import SearchSerializer   


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

        if "file" not in request.FILES:
            return Response(
                {"error": "No file provided"},
                status=400
            )

        file = request.FILES["file"]

        text = extract_text(file)

        cleaned_text = clean_text(text)

        chunks = chunk_text(cleaned_text)

        embeddings = generate_embeddings(chunks)

        document = Document.objects.create(
            filename=file.name,
            total_characters=len(cleaned_text),
            total_chunks=len(chunks)
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