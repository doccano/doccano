from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsSuperUser(BasePermission):
    """
    Custom permission to allow only superusers to access the view.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False  # If not authenticated, return default 403 response
        
        if not request.user.is_superuser:
            raise PermissionDenied(detail="Only superusers can create a user.")  # Custom error message
        
        return True