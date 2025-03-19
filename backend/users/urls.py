from django.urls import include, path
from users.views import UserRemove

from .views import Me, UserCreation, Users

urlpatterns = [
    path(route="me", view=Me.as_view(), name="me"),
    path(route="users", view=Users.as_view(), name="user_list"),
    path(route="users/create", view=UserCreation.as_view(), name="user_create"),
    path(route="users/remove/<int:id>", view=UserRemove.as_view(), name="user_remove"),
    path("auth/", include("dj_rest_auth.urls")),
]
