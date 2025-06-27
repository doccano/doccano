from rest_framework import permissions
from projects.models import Member
from django.conf import settings


class CanCreatePerspective(permissions.BasePermission):
    """
    Custom permission to allow only project admins to create/edit/delete questions.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        project_id = view.kwargs.get('project_id')
        if not project_id:
            return False
        
        # Check if user is project admin
        return Member.objects.filter(
            project_id=project_id,
            user=request.user,
            role__name=settings.ROLE_PROJECT_ADMIN
        ).exists()


class CanAnswerPerspective(permissions.BasePermission):
    """
    Custom permission to allow project members (except admins) to answer questions.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        project_id = view.kwargs.get('project_id')
        if not project_id:
            return False
        
        # Check if user is project member
        member = Member.objects.filter(
            project_id=project_id,
            user=request.user
        ).first()
        
        if not member:
            return False
        
        # Admins cannot answer
        if member.role.name == settings.ROLE_PROJECT_ADMIN:
            return False
        
        return True


class CanViewPerspective(permissions.BasePermission):
    """
    Custom permission to allow all project members to view questions.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        project_id = view.kwargs.get('project_id')
        if not project_id:
            return False
        
        # Check if user is project member
        return Member.objects.filter(
            project_id=project_id,
            user=request.user
        ).exists()
