from django.urls import path

from .views import AnnotationView, AnnotationAPIView, LabelAPIView

urlpatterns = [
    path('<int:project_id>/docs', AnnotationView.as_view()),
    path('<int:project_id>/apis/data', AnnotationAPIView.as_view()),
    path('<int:project_id>/apis/label', LabelAPIView.as_view()),
]
