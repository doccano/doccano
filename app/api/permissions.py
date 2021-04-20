from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Subquery
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAdminUser)

from .models import Project, Role, RoleMapping


class ProjectMixin:
    @classmethod
    def get_project_id(self, request, view):
        return view.kwargs.get('project_id') or request.query_params.get('project_id')


class IsAdminUserAndWriteOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return IsAdminUser().has_permission(request, view)


class ProjectAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or is_in_role(
            role_name=IsProjectAdmin.role_name,
            user_id=self.request.user.id,
            project_id=self.kwargs['project_id'],
        )


class IsOwnAnnotation(ProjectMixin, BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        project_id = self.get_project_id(request, view)
        annotation_id = view.kwargs.get('annotation_id')
        project = get_object_or_404(Project, pk=project_id)
        model = project.get_annotation_class()
        annotation = model.objects.filter(id=annotation_id, user=request.user)

        return annotation.exists()


class IsOwnComment(ProjectMixin, BasePermission):
    @classmethod
    def has_object_permission(cls, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.user.id == request.user.id


class RolePermission(ProjectMixin, BasePermission):
    UNSAFE_METHODS = ('POST', 'PATCH', 'DELETE')
    unsafe_methods_check = True
    role_name = ''

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if self.unsafe_methods_check and request.method in self.UNSAFE_METHODS:
            return request.user.is_superuser

        project_id = self.get_project_id(request, view)
        if not project_id and request.method in SAFE_METHODS:
            return True

        return is_in_role(self.role_name, request.user.id, project_id)


class IsProjectAdmin(RolePermission):
    unsafe_methods_check = False
    role_name = settings.ROLE_PROJECT_ADMIN


class IsAnnotatorAndReadOnly(RolePermission):
    role_name = settings.ROLE_ANNOTATOR


class IsAnnotator(RolePermission):
    unsafe_methods_check = False
    role_name = settings.ROLE_ANNOTATOR


class IsAnnotationApproverAndReadOnly(RolePermission):
    role_name = settings.ROLE_ANNOTATION_APPROVER


class IsAnnotationApprover(RolePermission):
    unsafe_methods_check = False
    role_name = settings.ROLE_ANNOTATION_APPROVER


def is_in_role(role_name, user_id, project_id):
    return RoleMapping.objects.filter(
        user_id=user_id,
        project_id=project_id,
        role_id=Subquery(Role.objects.filter(name=role_name).values('id')),
    ).exists()


IsInProjectReadOnlyOrAdmin = (IsAnnotatorAndReadOnly | IsAnnotationApproverAndReadOnly | IsProjectAdmin)
IsInProjectOrAdmin = (IsAnnotator | IsAnnotationApprover | IsProjectAdmin)
