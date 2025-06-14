# backend/labels/urls.py

from django.urls import path
from .views import (
    DiscrepancyMessageListAPI,
    RelationList, RelationDetail,
    CategoryListAPI, CategoryDetailAPI,
    SpanListAPI, SpanDetailAPI,
    TextLabelListAPI, TextLabelDetailAPI,
    BoundingBoxListAPI, BoundingBoxDetailAPI,
    SegmentationListAPI, SegmentationDetailAPI,
)

urlpatterns = [
    path(
        "examples/<int:example_id>/relations",
        RelationList.as_view(),
        name="relation_list",
    ),
    path(
        "examples/<int:example_id>/relations/<int:annotation_id>",
        RelationDetail.as_view(),
        name="relation_detail",
    ),

    # Rota para chat de discrepância do projeto
    path(
        "discrepancies/messages",
        DiscrepancyMessageListAPI.as_view(),
        name="discrepancy_messages",
    ),

    path(
        "examples/<int:example_id>/categories",
        CategoryListAPI.as_view(),
        name="category_list",
    ),
    path(
        "examples/<int:example_id>/categories/<int:annotation_id>",
        CategoryDetailAPI.as_view(),
        name="category_detail",
    ),

    path(
        "examples/<int:example_id>/spans",
        SpanListAPI.as_view(),
        name="span_list",
    ),
    path(
        "examples/<int:example_id>/spans/<int:annotation_id>",
        SpanDetailAPI.as_view(),
        name="span_detail",
    ),

    path(
        "examples/<int:example_id>/texts",
        TextLabelListAPI.as_view(),
        name="text_list",
    ),
    path(
        "examples/<int:example_id>/texts/<int:annotation_id>",
        TextLabelDetailAPI.as_view(),
        name="text_detail",
    ),

    path(
        "examples/<int:example_id>/bboxes",
        BoundingBoxListAPI.as_view(),
        name="bbox_list",
    ),
    path(
        "examples/<int:example_id>/bboxes/<int:annotation_id>",
        BoundingBoxDetailAPI.as_view(),
        name="bbox_detail",
    ),

    path(
        "examples/<int:example_id>/segments",
        SegmentationListAPI.as_view(),
        name="segmentation_list",
    ),
    path(
        "examples/<int:example_id>/segments/<int:annotation_id>",
        SegmentationDetailAPI.as_view(),
        name="segmentation_detail",
    ),
]
