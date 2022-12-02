from django.urls import path

from .views import Social

urlpatterns = [
    path("links/", Social.as_view()),
]
