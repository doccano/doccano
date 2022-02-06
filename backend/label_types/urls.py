from django.urls import path

from .views import CategoryTypeList, CategoryTypeDetail, CategoryTypeUploadAPI
from .views import SpanTypeList, SpanTypeDetail, SpanTypeUploadAPI
from .views import RelationTypeList, RelationTypeDetail, RelationTypeUploadAPI


urlpatterns = [
    path(route="category-types", view=CategoryTypeList.as_view(), name="category_types"),
    path(route="category-types/<int:label_id>", view=CategoryTypeDetail.as_view(), name="category_type"),
    path(route="span-types", view=SpanTypeList.as_view(), name="span_types"),
    path(route="span-types/<int:label_id>", view=SpanTypeDetail.as_view(), name="span_type"),
    path(route="category-type-upload", view=CategoryTypeUploadAPI.as_view(), name="category_type_upload"),
    path(route="span-type-upload", view=SpanTypeUploadAPI.as_view(), name="span_type_upload"),
    path(route="relation_types", view=RelationTypeList.as_view(), name="relation_types_list"),
    path(route="relation_type-upload", view=RelationTypeUploadAPI.as_view(), name="relation_type-upload"),
    path(route="relation_types/<int:relation_type_id>", view=RelationTypeDetail.as_view(), name="relation_type_detail"),
]
