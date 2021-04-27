from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .utils import create_default_roles


class TestFeatures(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_name = 'user_name'
        cls.user_pass = 'user_pass'
        create_default_roles()
        cls.user = User.objects.create_user(username=cls.user_name, password=cls.user_pass, email='fizz@buzz.com')

    def setUp(self):
        self.client.login(username=self.user_name, password=self.user_pass)

    @override_settings(CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER=None)
    def test_no_cloud_upload(self):
        response = self.client.get(reverse('features'))

        self.assertFalse(response.json().get('cloud_upload'))
