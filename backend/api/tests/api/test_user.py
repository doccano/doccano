from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .utils import create_default_roles


class TestUserAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        create_default_roles()
        User.objects.create_superuser(username=cls.super_user_name,
                                      password=cls.super_user_pass,
                                      email='fizz@buzz.com')
        cls.url = reverse(viewname='user_list')

    def test_returns_user_count(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(1, len(response.data))
