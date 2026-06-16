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


class StatsSerializer(serializers.Serializer):

    documents = serializers.IntegerField()

    total_chunks = serializers.IntegerField()

    average_quality = serializers.FloatField()


class DashboardSerializer(serializers.Serializer):

    documents = serializers.IntegerField()

    completed = serializers.IntegerField()

    failed = serializers.IntegerField()

    languages = serializers.ListField(
        child=serializers.CharField()
    )


class QualityReportSerializer(serializers.Serializer):

    documents = serializers.IntegerField()

    average_quality = serializers.FloatField()

    total_duplicates = serializers.IntegerField()

    languages = serializers.DictField()


    