from django.urls import path

from data_pipeline.views import UploadDocumentView, SearchView, DocumentListView, StatsView, QualityReportView, DashboardView, TopDocumentsView, DeleteDocumentView

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

        path(
        "quality-report/",
        QualityReportView.as_view(),
        name="quality-report"
    ),

        path(
        "dashboard/",
        DashboardView.as_view(),
        name="dashboard"
        ),

        path(
        "top-documents/",
        TopDocumentsView.as_view(),
        name="top-documents"
        ),

        path(
        "delete-document/<int:document_id>/",
        DeleteDocumentView.as_view(),
        name="delete-document"
        ),

]