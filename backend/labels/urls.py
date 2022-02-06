from django.urls import path

from .views import CategoryListAPI, CategoryDetailAPI
from .views import SpanListAPI, SpanDetailAPI
from .views import TextLabelListAPI, TextLabelDetailAPI
from .views import RelationList, RelationDetail


urlpatterns = [
    path(route="annotation_relations", view=RelationList.as_view(), name="relation_list"),
    path(route="annotation_relations/<int:annotation_id>", view=RelationDetail.as_view(), name="relation_detail"),
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
]
