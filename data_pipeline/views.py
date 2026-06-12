from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services.extractor import extract_text

# Create your views here.

class UploadDocumentView(APIView):

    def post(self, request):

        pdf_file = request.FILES.get("file")

        if not pdf_file:
            return Response(
                {"error": "No file provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        text = extract_text(pdf_file)

        return Response({
            "filename": pdf_file.name,
            "characters": len(text),
            "preview": text[:500]
        })