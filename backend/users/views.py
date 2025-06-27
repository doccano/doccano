from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import UserSerializer, UserDetailSerializer, RegisterSerializer


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
        return request.user and (request.user.is_staff or request.user.is_superuser)


class MeView(APIView):
    """
    API endpoint for the authenticated user to view their own details
    """

    permission_classes = [permissions.IsAuthenticated]
    swagger_tags = ['Current User']

    def get(self, request):
        serializer = UserDetailSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing users
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminWritePermission]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ("username",)
    search_fields = ("username", "email", "first_name", "last_name")
    ordering_fields = ("id", "username", "email", "is_staff", "is_superuser", "date_joined")
    ordering = ("username",)
    swagger_tags = ['Users']

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return UserDetailSerializer
        return UserSerializer

    def perform_update(self, serializer):
        if serializer.validated_data.get("is_superuser") and not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to make this user a superuser.")
        if serializer.validated_data.get("is_staff") and not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to make this user a staff member.")
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance == self.request.user:
            raise PermissionDenied("You cannot delete your own account.")
        if instance.is_superuser:
            raise ValidationError(f"User '{instance.username}' is an administrator and cannot be deleted.")
        if instance.is_staff:
            raise ValidationError(f"User '{instance.username}' is a staff member and cannot be deleted.")
        instance.delete()

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user


class RegisterView(CreateAPIView):
    """
    API endpoint for admin to register new users
    """
    serializer_class = RegisterSerializer
    permission_classes = [AdminWritePermission]  # Changed from AllowAny to AdminWritePermission
    swagger_tags = ['User Management']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Return user data without sensitive information
        return_serializer = UserSerializer(user)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            return_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
