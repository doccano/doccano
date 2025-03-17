from django.urls import include, path

from .views import Me, UserCreation, Users

urlpatterns = [
    path("me", Me.as_view(), name="me"),
    path("users", Users.as_view(), name="user_list"),
    path("users/create", UserCreation.as_view(), name="user_create"),
    path("auth/", include("dj_rest_auth.urls")),
]