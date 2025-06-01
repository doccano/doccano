from django.urls import path
from .views import (
    Groups, GroupDetail, GroupCreate,
    GroupPermissionsList, GroupPermissionsCreate, GroupPermissionsDetail,
    PermissionList, PermissionCreate, PermissionDetail
)

urlpatterns = [
    # Group URLs
    path(route="groups/<int:id>", view=GroupDetail.as_view(), name="group_detail"), 
    path(route="groups/create/", view=GroupCreate.as_view(), name="group_create"),
    path(route="groups", view=Groups.as_view(), name="group_list"),
    
    # GroupPermissions URLs
    path(route="group-permissions/<int:id>", view=GroupPermissionsDetail.as_view(), name="group_permissions_detail"),
    path(route="group-permissions/create/", view=GroupPermissionsCreate.as_view(), name="group_permissions_create"),
    path(route="group-permissions", view=GroupPermissionsList.as_view(), name="group_permissions_list"),
    
    # Permission URLs
    path(route="permissions/<int:id>", view=PermissionDetail.as_view(), name="permission_detail"),
    path(route="permissions/create/", view=PermissionCreate.as_view(), name="permission_create"),
    path(route="permissions", view=PermissionList.as_view(), name="permission_list"),
]
