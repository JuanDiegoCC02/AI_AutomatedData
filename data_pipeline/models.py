from django.db import models


# Create your models here.


class Document(models.Model):

    filename = models.CharField(max_length=255)

    total_characters = models.IntegerField()

    total_chunks = models.IntegerField(default=0)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename