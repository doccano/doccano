from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth import get_user_model

from .serializers import UserSerializer
from projects.permissions import IsProjectAdmin

User = get_user_model()

class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class Users(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        queryset = User.objects.all()
        search_query = self.request.query_params.get('q', None)
        if search_query:
            queryset = queryset.filter(username__icontains=search_query) | queryset.filter(email__icontains=search_query)
        return queryset


class UserCreation(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user
    

class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated & IsAdminUser]
    lookup_field = 'id'  
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_delete(self, instance):
        instance.delete()

