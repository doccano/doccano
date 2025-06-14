from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.okta.views import OktaOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView


class OktaLogin(SocialLoginView):
    adapter_class = OktaOAuth2Adapter
    callback_url = "/projects"
    client_class = OAuth2Client
