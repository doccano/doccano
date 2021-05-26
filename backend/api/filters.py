from django.db.models import Count, Q
from django_filters.rest_framework import BooleanFilter, FilterSet

from .models import Example


class DocumentFilter(FilterSet):
    spans__isnull = BooleanFilter(field_name='spans', method='filter_annotations')
    categories__isnull = BooleanFilter(field_name='categories', method='filter_annotations')
    texts__isnull = BooleanFilter(field_name='texts', method='filter_annotations')

    def filter_annotations(self, queryset, field_name, value):
        queryset = queryset.annotate(num_annotations=Count(
            expression=field_name,
            filter=Q(**{f"{field_name}__user": self.request.user}) | Q(project__collaborative_annotation=True)
            )
        )

        should_have_annotations = not value
        if should_have_annotations:
            queryset = queryset.filter(num_annotations__gte=1)
        else:
            queryset = queryset.filter(num_annotations__lte=0)

        return queryset

    class Meta:
        model = Example
        fields = (
            'project', 'text', 'created_at', 'updated_at',
            'categories__label__id', 'spans__label__id',
            'categories__isnull', 'spans__isnull', 'texts__isnull'
        )
