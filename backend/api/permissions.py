from rest_framework.permissions import BasePermission


class CanEditAnnotation(BasePermission):

    def __init__(self, queryset):
        super().__init__()
        self.queryset = queryset

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        annotation_id = view.kwargs.get('annotation_id')
        return self.queryset.filter(id=annotation_id, user=request.user).exists()


class IsOwnComment(BasePermission):
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
