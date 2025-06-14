from rest_framework.permissions import BasePermission


class IsOwnComment(BasePermission):
    @classmethod
    def has_object_permission(cls, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.user.id == request.user.id
