from rest_framework import serializers
from .models import Document

# Create your serializers here.

class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = "__all__"