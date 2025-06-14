from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from api.middleware import HeaderAuthMiddleware


@override_settings(HEADER_AUTH_USER_GROUPS="X-AuthProxy-Groups")
@override_settings(HEADER_AUTH_ADMIN_GROUP_NAME="Admin")
@override_settings(HEADER_AUTH_GROUPS_SEPERATOR=";")
class HeaderAuthMiddlewareTest(TestCase):
    def test_process_user_groups_is_super(self):
        user = User.objects.create_user(username="TestUser")
        user.is_superuser = False

        get_response = mock.MagicMock()

        middleware = HeaderAuthMiddleware(get_response)
        middleware.process_user_groups(user, {"HTTP_X_AUTHPROXY_GROUPS": "Admin;Reader"})

        self.assertTrue(user.is_superuser)

    def test_process_user_groups_is_not_super(self):
        user = User.objects.create_user(username="TestUser")
        user.is_superuser = True

        get_response = mock.MagicMock()

        middleware = HeaderAuthMiddleware(get_response)
        middleware.process_user_groups(user, {"HTTP_X_AUTHPROXY_GROUPS": "Guest;Reader"})

        self.assertFalse(user.is_superuser)
