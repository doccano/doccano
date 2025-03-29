from django.urls import path
from .views import PerspectiveView

urlpatterns = [
    path(
        "projects/<int:project_id>/perspectives/",
        PerspectiveView.as_view({"get": "list", "post": "create"}),
        name="project-perspectives",
    ),
]