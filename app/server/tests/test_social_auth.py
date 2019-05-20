from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from social_core.backends.github import GithubOAuth2
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
