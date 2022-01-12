from django.urls import path

from .views import MemberDetail, MemberList, Roles

urlpatterns = [
    path(
        route='roles',
        view=Roles.as_view(),
        name='roles'
    ),
    path(
        route='projects/<int:project_id>/members',
        view=MemberList.as_view(),
        name='member_list'
    ),
    path(
        route='projects/<int:project_id>/members/<int:member_id>',
        view=MemberDetail.as_view(),
        name='member_detail'
    )
]
