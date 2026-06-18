import django_filters

from .models import Document


class DocumentFilter(
    django_filters.FilterSet
):

    language = django_filters.CharFilter(
        lookup_expr="iexact"
    )

    status = django_filters.CharFilter(
        lookup_expr="iexact"
    )

    class Meta:

        model = Document

        fields = [
            "language",
            "status"
        ]