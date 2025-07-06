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
    DatasetDetailsAPI,
    DatasetTextsAPI,
    PerspectiveAnswersAPI,
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
    path(route="dataset-details", view=DatasetDetailsAPI.as_view(), name="dataset_details"),
    path(route="dataset-texts", view=DatasetTextsAPI.as_view(), name="dataset_texts"),
    path(route="perspective-answers/<int:question_id>", view=PerspectiveAnswersAPI.as_view(), name="perspective_answers"),
    path(route="export", view=ExportReportsAPI.as_view(), name="export_reports"),
]
