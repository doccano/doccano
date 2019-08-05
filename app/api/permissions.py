from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Subquery
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser

from .models import Project, Role, RoleMapping


class ProjectMixin:
    def get_project_id(self, request, view):
        return view.kwargs.get('project_id') or request.query_params.get('project_id')


class IsProjectUser(ProjectMixin, BasePermission):

    def has_permission(self, request, view):
        project = get_object_or_404(Project, pk=self.get_project_id(request, view))
        return user in project.users.all()


class IsAdminUserAndWriteOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return IsAdminUser().has_permission(request, view)


class SuperUserMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


class IsOwnAnnotation(ProjectMixin, BasePermission):

    def has_permission(self, request, view):
        project_id = self.get_project_id(request, view)
        annotation_id = view.kwargs.get('annotation_id')
        project = get_object_or_404(Project, pk=project_id)
        model = project.get_annotation_class()
        annotation = model.objects.filter(id=annotation_id, user=request.user)

        return annotation.exists()


class RolePermission(ProjectMixin, BasePermission):
    UNSAFE_METHODS = ('POST', 'PATCH', 'DELETE')
    unsafe_methods_check = True
    role_name = ''

    def is_super_user(self, user):
        return user.is_superuser

    def has_permission(self, request, view):
        is_super_user = self.is_super_user(request.user)
        if is_super_user:
            return True

        if self.unsafe_methods_check and request.method in self.UNSAFE_METHODS:
            return is_super_user

        project_id = self.get_project_id(request, view)
        if not project_id and request.method in SAFE_METHODS:
            return True

        return is_in_role(self.role_name, request.user.id, project_id)


class IsProjectAdmin(RolePermission):
    unsafe_methods_check = False
    role_name = settings.ROLE_PROJECT_ADMIN


class IsAnnotatorAndCreator(RolePermission):
    unsafe_methods_check = False
    role_name = settings.ROLE_ANNOTATOR


class IsAnnotator(RolePermission):
    role_name = settings.ROLE_ANNOTATOR


class IsAnnotationApprover(RolePermission):
    role_name = settings.ROLE_ANNOTATION_APPROVER


def is_in_role(role_name, user_id, project_id):
    return RoleMapping.objects.filter(
        user_id=user_id,
        project_id=project_id,
        role_id=Subquery(Role.objects.filter(name=role_name).values('id')),
    ).exists()
