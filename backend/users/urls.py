from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MeView, RegisterView

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("me", MeView.as_view(), name="me"),
    path("register", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
    path("auth/", include("dj_rest_auth.urls")),
]
