from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser

from .models import Project


class IsProjectUser(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        project_id = view.kwargs.get('project_id') or request.query_params.get('project_id')
        project = get_object_or_404(Project, pk=project_id)

        return user in project.users.all()


class IsAdminUserAndWriteOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return IsAdminUser().has_permission(request, view)


class SuperUserMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


class IsOwnAnnotation(BasePermission):

    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id')
        annotation_id = view.kwargs.get('annotation_id')
        project = get_object_or_404(Project, pk=project_id)
        model = project.get_annotation_class()
        annotation = model.objects.filter(id=annotation_id, user=request.user)

        return annotation.exists()
