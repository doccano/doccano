from django.urls import path

from .views import (
    CategoryTypeDistribution,
    MemberProgressAPI,
    ProgressAPI,
    RelationTypeDistribution,
    SpanTypeDistribution,
    DiscrepancyStatsAPI,
    PerspectiveStatsAPI,
    LabelStatsAPI,
    ExportReportsAPI,
)

urlpatterns = [
    path(route="progress", view=ProgressAPI.as_view(), name="progress"),
    path(route="member-progress", view=MemberProgressAPI.as_view(), name="member_progress"),
    path(route="category-distribution", view=CategoryTypeDistribution.as_view(), name="category_distribution"),
    path(route="relation-distribution", view=RelationTypeDistribution.as_view(), name="relation_distribution"),
    path(route="span-distribution", view=SpanTypeDistribution.as_view(), name="span_distribution"),
    path(route="discrepancy-stats", view=DiscrepancyStatsAPI.as_view(), name="discrepancy_stats"),
    path(route="perspective-stats", view=PerspectiveStatsAPI.as_view(), name="perspective_stats"),
    path(route="label-stats", view=LabelStatsAPI.as_view(), name="label_stats"),
    path(route="export", view=ExportReportsAPI.as_view(), name="export_reports"),
]
