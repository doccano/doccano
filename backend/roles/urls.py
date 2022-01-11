from django.urls import path

from .views import RoleMappingDetail, RoleMappingList, Roles

urlpatterns = [
    path(
        route='roles',
        view=Roles.as_view(),
        name='roles'
    ),
    path(
        route='projects/<int:project_id>/roles',
        view=RoleMappingList.as_view(),
        name='rolemapping_list'
    ),
    path(
        route='projects/<int:project_id>/roles/<int:rolemapping_id>',
        view=RoleMappingDetail.as_view(),
        name='rolemapping_detail'
    )
]
