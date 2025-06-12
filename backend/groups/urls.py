from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, PermissionViewSet, ContentTypeViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'content-types', ContentTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
