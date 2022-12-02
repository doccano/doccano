from django.urls import path

from .okta import OktaLogin

urlpatterns = [
    path("complete/okta-oauth2/", OktaLogin.as_view(), name="okta_login"),
]
