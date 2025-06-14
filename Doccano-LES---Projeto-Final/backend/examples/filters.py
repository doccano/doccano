from django.db.models import Count, Q, QuerySet
from django_filters.rest_framework import BooleanFilter, CharFilter, FilterSet

from .models import Example


class ExampleFilter(FilterSet):
    confirmed = BooleanFilter(field_name="states", method="filter_by_state")
    label = CharFilter(method="filter_by_label")
    assignee = CharFilter(method="filter_by_assignee")

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

    def filter_by_label(self, queryset: QuerySet, field_name: str, label: str) -> QuerySet:
        """Filter examples by a given label name.

        This performs filtering on all of the following labels at once:
        - categories
        - spans
        - relations
        - bboxes
        - segmentations

        Todo: Consider project type to make filtering more efficient.

        Args:
            queryset (QuerySet): QuerySet to filter.
            field_name (str): This equals to `label`.
            label (str): The label name to filter.

        Returns:
            QuerySet: Filtered examples.
        """
        queryset = queryset.filter(
            Q(categories__label__text=label)
            | Q(spans__label__text=label)
            | Q(relations__type__text=label)
            | Q(bboxes__label__text=label)
            | Q(segmentations__label__text=label)
        )
        return queryset

    def filter_by_assignee(self, queryset: QuerySet, field_name: str, assignee: str) -> QuerySet:
        return queryset.filter(assignments__assignee__username=assignee)

    class Meta:
        model = Example
        fields = ("project", "text", "created_at", "updated_at", "label", "assignee")
