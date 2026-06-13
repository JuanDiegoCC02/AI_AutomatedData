from django.urls import path

from data_pipeline.views import UploadDocumentView, SearchView, DocumentListView, StatsView

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

        path(
        "documents/",
        DocumentListView.as_view()
    ),

        path(
        "stats/",
        StatsView.as_view(),
        name="stats"
    ),


]