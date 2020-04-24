from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from social_core.backends.azuread_tenant import AzureADTenantOAuth2
from social_core.backends.github import GithubOAuth2
from social_core.backends.okta import OktaOAuth2
from social_core.backends.okta_openidconnect import OktaOpenIdConnect
from vcr_unittest import VCRMixin

from .. import social_auth

User = get_user_model()


class VCRTestCase(VCRMixin, TestCase):
    @property
    def access_token(self):
        raise NotImplementedError()

    def _get_vcr(self, **kwargs):
        kwargs['decode_compressed_response'] = True
        kwargs['record_mode'] = 'none' if self.access_token == 'censored' else 'all'
        return super()._get_vcr(**kwargs)

    def _get_vcr_kwargs(self, **kwargs):
        kwargs['filter_headers'] = ['Authorization']
        return super()._get_vcr_kwargs(**kwargs)


@override_settings(GITHUB_ADMIN_ORG_NAME='CatalystCode')
@override_settings(GITHUB_ADMIN_TEAM_NAME='doccano-dev')
class TestGithubSocialAuth(VCRTestCase):
    strategy = None
    backend = GithubOAuth2(strategy=strategy)
    access_token = 'censored'

    def test_fetch_permissions_is_admin(self):
        user = User()

        social_auth.fetch_github_permissions(
            strategy=self.strategy,
            details={'username': 'c-w'},
            user=user,
            backend=self.backend,
            response={'access_token': self.access_token},
        )

        self.assertTrue(user.is_superuser)

    def test_fetch_permissions_not_admin(self):
        user = User()

        social_auth.fetch_github_permissions(
            strategy=self.strategy,
            details={'username': 'hirosan'},
            user=user,
            backend=self.backend,
            response={'access_token': self.access_token},
        )

        self.assertFalse(user.is_superuser)


@override_settings(SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY='aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa')
@override_settings(SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb=')
@override_settings(SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT='cccccccc-cccc-cccc-cccc-cccccccccccc')
class TestAzureADTenantSocialAuth(VCRTestCase):
    strategy = None
    backend = AzureADTenantOAuth2(strategy=strategy)
    access_token = 'censored'

    @override_settings(AZUREAD_ADMIN_GROUP_ID='dddddddd-dddd-dddd-dddd-dddddddddddd')
    def test_fetch_permissions_is_admin(self):
        user = User()

        social_auth.fetch_azuread_permissions(
            strategy=self.strategy,
            details={},
            user=user,
            backend=self.backend,
            response={'access_token': self.access_token},
        )

        self.assertTrue(user.is_superuser)

    @override_settings(AZUREAD_ADMIN_GROUP_ID='eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee')
    def test_fetch_permissions_not_admin(self):
        user = User()

        social_auth.fetch_azuread_permissions(
            strategy=self.strategy,
            details={},
            user=user,
            backend=self.backend,
            response={'access_token': self.access_token},
        )

        self.assertFalse(user.is_superuser)


@override_settings(SOCIAL_AUTH_OKTA_OAUTH2_KEY='0000000000aaaaaaaaaa')  # nosec
@override_settings(SOCIAL_AUTH_OKTA_OAUTH2_SECRET='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb=')  # nosec
@override_settings(SOCIAL_AUTH_OKTA_OAUTH2_API_URL='https://dev-000000.okta.com/oauth2')  # nosec
@override_settings(OKTA_OAUTH2_ADMIN_GROUP_NAME='admin-group')
class TestOktaOAuth2SocialAuth(VCRTestCase):
    strategy = None
    backend = OktaOAuth2(strategy=strategy)
    access_token = 'censored'

    def test_fetch_permissions_is_admin(self):
        user = User()

        social_auth.fetch_okta_oauth2_permissions(
            strategy=self.strategy,
            details={},
            user=user,
            backend=self.backend,
            response={'access_token': self.access_token},
        )

        self.assertTrue(user.is_superuser)

    def test_fetch_permissions_not_admin(self):
        user = User()

        social_auth.fetch_okta_oauth2_permissions(
            strategy=self.strategy,
            details={},
            user=user,
            backend=self.backend,
            response={'access_token': self.access_token},
        )

        self.assertFalse(user.is_superuser)


@override_settings(SOCIAL_AUTH_OKTA_OPENIDCONNECT_KEY='0000000000aaaaaaaaaa')  # nosec
@override_settings(SOCIAL_AUTH_OKTA_OPENIDCONNECT_SECRET='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb=')  # nosec
@override_settings(SOCIAL_AUTH_OKTA_OPENIDCONNECT_API_URL='https://dev-000000.okta.com/oauth2')  # nosec
@override_settings(OKTA_OPENIDCONNECT_ADMIN_GROUP_NAME='admin-group')
class TestOktaOpenIdConnectSocialAuth(VCRTestCase):
    strategy = None
    backend = OktaOpenIdConnect(strategy=strategy)
    access_token = 'censored'

    def test_fetch_permissions_is_admin(self):
        user = User()

        social_auth.fetch_okta_openidconnect_permissions(
            strategy=self.strategy,
            details={},
            user=user,
            backend=self.backend,
            response={'access_token': self.access_token},
        )

        self.assertTrue(user.is_superuser)

    def test_fetch_permissions_not_admin(self):
        user = User()

        social_auth.fetch_okta_openidconnect_permissions(
            strategy=self.strategy,
            details={},
            user=user,
            backend=self.backend,
            response={'access_token': self.access_token},
        )

        self.assertFalse(user.is_superuser)
