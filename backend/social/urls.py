from django.urls import include, path

from .okta import OktaLogin
from .views import Social

urlpatterns = [
    path('links/', Social.as_view()),
    path('complete/okta-oauth2/', OktaLogin.as_view(), name='okta_login'),
]
