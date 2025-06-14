from rest_framework.permissions import BasePermission


class CanEditLabel(BasePermission):
    def __init__(self, queryset):
        super().__init__()
        self.queryset = queryset

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        annotation_id = view.kwargs.get("annotation_id")
        return self.queryset.filter(id=annotation_id, user=request.user).exists()
