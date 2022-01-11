from rest_framework.permissions import BasePermission


class ProjectMixin:
    @classmethod
    def get_project_id(cls, request, view):
        return view.kwargs.get('project_id') or request.query_params.get('project_id')


class CanEditAnnotation(ProjectMixin, BasePermission):

    def __init__(self, queryset):
        super().__init__()
        self.queryset = queryset

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        annotation_id = view.kwargs.get('annotation_id')
        return self.queryset.filter(id=annotation_id, user=request.user).exists()


class IsOwnComment(ProjectMixin, BasePermission):
    @classmethod
    def has_object_permission(cls, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.user.id == request.user.id


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False
