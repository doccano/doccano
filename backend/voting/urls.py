from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VotingConfigurationViewSet

router = DefaultRouter()
router.register(r'voting', VotingConfigurationViewSet, basename='voting')

urlpatterns = [
    path('', include(router.urls)),
]
