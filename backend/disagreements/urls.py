from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisagreementViewSet

router = DefaultRouter()
router.register(r'disagreements', DisagreementViewSet, basename='disagreement')

urlpatterns = [
    path('', include(router.urls)),
]