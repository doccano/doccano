from django_filters.rest_framework import FilterSet, BooleanFilter
from .models import Document


class DocumentFilter(FilterSet):
    seq_annotations__isnull = BooleanFilter(field_name='seq_annotations', lookup_expr='isnull')
    doc_annotations__isnull = BooleanFilter(field_name='doc_annotations', lookup_expr='isnull')
    seq2seq_annotations__isnull = BooleanFilter(field_name='seq2seq_annotations', lookup_expr='isnull')

    class Meta:
        model = Document
        fields = ('project', 'text', 'meta', 'created_at', 'updated_at',
                  'doc_annotations__label__id', 'seq_annotations__label__id',
                  'doc_annotations__isnull', 'seq_annotations__isnull', 'seq2seq_annotations__isnull')
