from rest_framework import serializers
from .models import Document 
from rest_framework import serializers

# Create your serializers here.

class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = "__all__"



class SearchSerializer(serializers.Serializer):
    query = serializers.CharField()