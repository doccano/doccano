from django.test import RequestFactory, TestCase, override_settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from rest_framework import status
from ..forms import SignupForm
from ..tokens import account_activation_token
import re


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestActivate(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

        request_POST = {'username': 'username5648',
                        'email': 'email@example.com',
                        'password1': 'pwd0000Y00$$',
                        'password2': 'pwd0000Y00$$'}
        user = SignupForm(request_POST).save(commit=False)
        user.save()
        self.token = account_activation_token.make_token(user)
        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()

    def test_activate_invalid(self):
        response = self.client.get(reverse('activate', args=['wrong_uid', 'wrong_token']))
        self.assertEqual(response.status_code, 200)
        needle = '<p>Activation link is invalid!</p>'
        m = re.search(needle, str(response.content))
        self.assertTrue(m is None)

    def test_activate_valid(self):
        """we make sure code is for the /projects redirection"""
        response = self.client.get(reverse('activate', args=[self.uid, self.token]))
        # For some reason this get rejected by Travis CI
        # File "/usr/local/lib/python3.6/site-packages/webpack_loader/loader.py", line 26, in _load_assets with open(self.config['STATS_FILE'], encoding="utf-8") as f:
        # FileNotFoundError: [Errno 2] No such file or directory: '/doccano/app/server/static/webpack-stats.json'
        # self.assertRedirects(response, '/projects/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
