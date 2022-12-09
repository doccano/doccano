from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


class Social(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "okta": {
                    "type": "oauth2",
                    "base_url": settings.SOCIALACCOUNT_PROVIDERS.get("okta").get("OKTA_BASE_URL"),
                    "client_id": settings.SOCIALACCOUNT_PROVIDERS.get("okta").get("APP").get("client_id"),
                    "redirect_path": "/social/complete/okta-oauth2",
                    "authorize_url": "https://"
                    + settings.SOCIALACCOUNT_PROVIDERS.get("okta").get("OKTA_BASE_URL")
                    + "/oauth2/v1/authorize?response_type=code&client_id="
                    + settings.SOCIALACCOUNT_PROVIDERS.get("okta").get("APP").get("client_id")
                    + "&scope=openid&state=unknown&response_mode=form_post",
                }
                if settings.SOCIALACCOUNT_PROVIDERS.get("okta").get("OKTA_BASE_URL")
                else {},
            }
        )
