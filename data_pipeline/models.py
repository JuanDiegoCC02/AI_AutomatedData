from django.db import models


# Create your models here.


class Document(models.Model):

    filename = models.CharField(max_length=255)

    total_characters = models.IntegerField()

    total_chunks = models.IntegerField(default=0)

    processing_time = models.FloatField(default=0)

    quality_score = models.FloatField(default=0)

    duplicate_chunks = models.IntegerField(default=0)

    language = models.CharField(max_length=20, default="unknown")

    status = models.CharField(
    max_length=50,
    default="COMPLETED",
    choices=[
        ("PENDING", "PENDING"),
        ("PROCESSING", "PROCESSING"),
        ("COMPLETED", "COMPLETED"),
        ("FAILED", "FAILED"),
     ]
    )   

    complexity_score = models.FloatField(default=0)

    user_id = models.CharField(max_length=255, null=True, blank=True)

    processed_at = models.DateTimeField(null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    file_size = models.IntegerField(default=0) 

    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.filename