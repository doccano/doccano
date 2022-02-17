from django.urls import include, path

from .views import DatasetCatalog, DatasetImportAPI

urlpatterns = [
    path("fp/", include("django_drf_filepond.urls")),
    path(route="projects/<int:project_id>/upload", view=DatasetImportAPI.as_view(), name="upload"),
    path(route="projects/<int:project_id>/catalog", view=DatasetCatalog.as_view(), name="catalog"),
]
