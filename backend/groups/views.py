from rest_framework import viewsets, permissions, filters
from django.contrib.auth.models import Group, Permission, ContentType
from .serializers import GroupSerializer, PermissionSerializer, ContentTypeSerializer

class AdminWritePermission(permissions.BasePermission):
    """
    Custom permission to allow only admins to create, update or delete objects.
    All authenticated users can read.
    """
    def has_permission(self, request, view):
        # Allow read-only for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # For write operations, require admin status
        return request.user and request.user.is_staff

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing user groups
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AdminWritePermission]
    swagger_tags = ['Groups']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'name']
    ordering = ['name']

class PermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoints for viewing permissions
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [AdminWritePermission]
    swagger_tags = ['Permissions']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'name', 'codename', 'content_type']
    ordering = ['content_type', 'codename']

class ContentTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoints for viewing content types
    """
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    permission_classes = [AdminWritePermission]
    swagger_tags = ['Content Types']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'app_label', 'model']
    ordering = ['app_label', 'model']