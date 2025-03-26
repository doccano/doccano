from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .serializers import UserSerializer, UserDetailSerializer
from projects.permissions import IsProjectAdmin


class Me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserDetailSerializer(request.user, context={"request": request})
        return Response(serializer.data)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_url_kwarg = "user_id"
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsAdminUser)]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("username",)
    def get_queryset(self):
        return self.queryset
    def perform_update(self, serializer):
        if serializer.validated_data.get("is_superuser") and not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to make this user a superuser.")
        if serializer.validated_data.get("is_staff") and not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to make this user a staff member.")
        return super().perform_update(serializer)
    def perform_destroy(self, instance):
        if instance == self.request.user:
            raise PermissionDenied("You cannot delete your own account.")
        instance.delete()

class Users(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("username",)
    ordering_fields = ("username", "email", "is_staff", "is_superuser")
    ordering = ("username",)  # Default ordering
    # Direction can be controlled by using "-" prefix (e.g., "-username" for descending)


class UserCreation(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsAdminUser)]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user
