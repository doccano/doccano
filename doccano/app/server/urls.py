from django.urls import path

from .views import AnnotationView, AnnotationAPIView, LabelAPIView

urlpatterns = [
    path('', AnnotationView.as_view()),
    path('api/annotation/', AnnotationAPIView.as_view()),
    path('api/label/', LabelAPIView.as_view()),
]
