from django.urls import path

from data_pipeline.views import UploadDocumentView

# Create your urls here.

urlpatterns = [
        path(
        "upload-document/",
        UploadDocumentView.as_view(),
        name="upload-document"
    ),

]