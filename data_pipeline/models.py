from django.db import models

# Create your models here.

from django.db import models


class Document(models.Model):

    filename = models.CharField(max_length=255)

    total_characters = models.IntegerField()

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename