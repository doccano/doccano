from django.urls import path

from .views import (
    BoundingBoxDetailAPI,
    BoundingBoxListAPI,
    CategoryDetailAPI,
    CategoryListAPI,
    RelationDetail,
    RelationList,
    SegmentationDetailAPI,
    SegmentationListAPI,
    SpanDetailAPI,
    SpanListAPI,
    TextLabelDetailAPI,
    TextLabelListAPI,
)

urlpatterns = [
    path(route="examples/<int:example_id>/relations", view=RelationList.as_view(), name="relation_list"),
    path(
        route="examples/<int:example_id>/relations/<int:annotation_id>",
        view=RelationDetail.as_view(),
        name="relation_detail",
    ),
    path(route="examples/<int:example_id>/categories", view=CategoryListAPI.as_view(), name="category_list"),
    path(
        route="examples/<int:example_id>/categories/<int:annotation_id>",
        view=CategoryDetailAPI.as_view(),
        name="category_detail",
    ),
    path(route="examples/<int:example_id>/spans", view=SpanListAPI.as_view(), name="span_list"),
    path(route="examples/<int:example_id>/spans/<int:annotation_id>", view=SpanDetailAPI.as_view(), name="span_detail"),
    path(route="examples/<int:example_id>/texts", view=TextLabelListAPI.as_view(), name="text_list"),
    path(
        route="examples/<int:example_id>/texts/<int:annotation_id>",
        view=TextLabelDetailAPI.as_view(),
        name="text_detail",
    ),
    path(route="examples/<int:example_id>/bboxes", view=BoundingBoxListAPI.as_view(), name="bbox_list"),
    path(
        route="examples/<int:example_id>/bboxes/<int:annotation_id>",
        view=BoundingBoxDetailAPI.as_view(),
        name="bbox_detail",
    ),
    path(route="examples/<int:example_id>/segments", view=SegmentationListAPI.as_view(), name="segmentation_list"),
    path(
        route="examples/<int:example_id>/segments/<int:annotation_id>",
        view=SegmentationDetailAPI.as_view(),
        name="segmentation_detail",
    ),
]
