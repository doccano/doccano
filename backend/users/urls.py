from django.urls import include, path

from .views import Me, Users

urlpatterns = [
    path(route="me", view=Me.as_view(), name="me"),
    path(route="users", view=Users.as_view(), name="user_list"),
    path("auth/", include("dj_rest_auth.urls")),
]
