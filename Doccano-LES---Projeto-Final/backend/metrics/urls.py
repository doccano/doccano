from django.urls import path

from .views import (
    CategoryTypeDistribution,
    CategoryTypePercentage,
    DisagreementStatsAPI,
    MemberProgressAPI,
    ProgressAPI,
    RelationTypeDistribution,
    RelationTypePercentage,
    SpanTypeDistribution,
    SpanTypePercentage,
)

urlpatterns = [
    path(route="progress", view=ProgressAPI.as_view(), name="progress"),
    path(route="member-progress", view=MemberProgressAPI.as_view(), name="member_progress"),
    path(route="category-distribution", view=CategoryTypeDistribution.as_view(), name="category_distribution"),
    path(route="relation-distribution", view=RelationTypeDistribution.as_view(), name="relation_distribution"),
    path(route="span-distribution", view=SpanTypeDistribution.as_view(), name="span_distribution"),
    path(route="category-percentage", view=CategoryTypePercentage.as_view(), name="category_percentage"),
    path(route="relation-percentage", view=RelationTypePercentage.as_view(), name="relation_percentage"),
    path(route="span-percentage", view=SpanTypePercentage.as_view(), name="span_percentage"),
    path(route="disagreement-stats", view=DisagreementStatsAPI.as_view(), name="disagreement_stats"),
]
