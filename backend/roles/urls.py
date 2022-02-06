from django.urls import path

from .views import Roles

urlpatterns = [path(route="roles", view=Roles.as_view(), name="roles")]
