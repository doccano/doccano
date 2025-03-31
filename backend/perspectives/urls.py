from django.urls import path
from .views import PerspectiveView

urlpatterns = [
    path(
        "projects/<int:project_id>/perspectives/",
        PerspectiveView.as_view({"get": "list", "post": "create"}),
        name="project-perspectives",
    ),
    path(
        "projects/<int:project_id>/perspectives/<int:pk>/",
        PerspectiveView.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="project-perspective-detail",
    ),
]