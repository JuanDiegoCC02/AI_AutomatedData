from django.urls import path

from data_pipeline.views import UploadDocumentView, SearchView

# Create your urls here.

urlpatterns = [
        path(
        "upload-document/",
        UploadDocumentView.as_view(),
        name="upload-document"
    ),

        path(
        "search/",
        SearchView.as_view(),
        name="search"
    ),

]