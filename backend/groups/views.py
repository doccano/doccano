from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from .models import Group, GroupPermissions, Permission
from .serializers import GroupSerializer, GroupCreateSerializer, GroupPermissionsSerializer, PermissionSerializer
from projects.permissions import IsProjectAdmin

class Groups(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name",)
    ordering_fields = ("id", "name")
    ordering = ("name",)  # Default ordering

class GroupCreate(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupCreateSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    
class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    lookup_field = 'id'

class GroupPermissionsList(generics.ListAPIView):
    queryset = GroupPermissions.objects.all()
    serializer_class = GroupPermissionsSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('group_id', 'permission_id')
    ordering_fields = ('id',)

class GroupPermissionsCreate(generics.CreateAPIView):
    queryset = GroupPermissions.objects.all()
    serializer_class = GroupPermissionsSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]

class GroupPermissionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupPermissions.objects.all()
    serializer_class = GroupPermissionsSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    lookup_field = 'id'

class PermissionList(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'codename')
    ordering_fields = ('id', 'name', 'codename')
    ordering = ('name',)

class PermissionCreate(generics.CreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]

class PermissionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    lookup_field = 'id'
