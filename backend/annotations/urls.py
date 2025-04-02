from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnotationView

router = DefaultRouter()
router.register(r'', AnnotationView, basename='annotation')

urlpatterns = [
    path('', include(router.urls)),
]