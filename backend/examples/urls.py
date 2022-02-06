from django.urls import path

from .views.example import ExampleList, ExampleDetail
from .views.comment import CommentList, CommentDetail
from .views.example_state import ExampleStateList


urlpatterns = [
    path(route="examples", view=ExampleList.as_view(), name="example_list"),
    path(route="examples/<int:example_id>", view=ExampleDetail.as_view(), name="example_detail"),
    path(route="comments", view=CommentList.as_view(), name="comment_list"),
    path(route="comments/<int:comment_id>", view=CommentDetail.as_view(), name="comment_detail"),
    path(route="examples/<int:example_id>/states", view=ExampleStateList.as_view(), name="example_state_list"),
]
