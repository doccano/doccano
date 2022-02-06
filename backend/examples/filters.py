from django.db.models import Count, Q
from django_filters.rest_framework import BooleanFilter, FilterSet

from .models import Example


class ExampleFilter(FilterSet):
    confirmed = BooleanFilter(field_name="states", method="filter_by_state")

    def filter_by_state(self, queryset, field_name, is_confirmed: bool):
        queryset = queryset.annotate(
            num_confirm=Count(
                expression=field_name,
                filter=Q(**{f"{field_name}__confirmed_by": self.request.user})
                | Q(project__collaborative_annotation=True),
            )
        )
        if is_confirmed:
            queryset = queryset.filter(num_confirm__gte=1)
        else:
            queryset = queryset.filter(num_confirm__lte=0)
        return queryset

    class Meta:
        model = Example
        fields = ("project", "text", "created_at", "updated_at")
