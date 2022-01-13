from django.urls import path

from .views import MemberList, MemberDetail

urlpatterns = [
    path(
        route='members',
        view=MemberList.as_view(),
        name='member_list'
    ),
    path(
        route='members/<int:member_id>',
        view=MemberDetail.as_view(),
        name='member_detail'
    )
]
