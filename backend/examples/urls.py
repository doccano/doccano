from django.urls import path

from .views.assignment import AssignmentDetail, AssignmentList
from .views.comment import CommentDetail, CommentList
from .views.example import ExampleDetail, ExampleList
from .views.example_state import ExampleStateList

urlpatterns = [
    path(route="assignments", view=AssignmentList.as_view(), name="assignment_list"),
    path(route="assignments/<uuid:assignment_id>", view=AssignmentDetail.as_view(), name="assignment_detail"),
    path(route="examples", view=ExampleList.as_view(), name="example_list"),
    path(route="examples/<int:example_id>", view=ExampleDetail.as_view(), name="example_detail"),
    path(route="comments", view=CommentList.as_view(), name="comment_list"),
    path(route="comments/<int:comment_id>", view=CommentDetail.as_view(), name="comment_detail"),
    path(route="examples/<int:example_id>/states", view=ExampleStateList.as_view(), name="example_state_list"),
]
