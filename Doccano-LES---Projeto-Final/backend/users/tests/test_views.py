from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .utils import make_user


class TestUserAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = make_user(username="bob")
        cls.url = reverse(viewname="user_list")

    def test_allows_authenticated_user_to_get_users(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], self.user.username)

    def test_denies_unauthenticated_user_to_get_users(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestMeAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = make_user(username="bob")
        cls.url = reverse(viewname="me")

    def test_return_own_information(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.data["id"], self.user.id)
        self.assertEqual(response.data["username"], self.user.username)

    def test_does_not_return_information_to_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUserCreationAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff = make_user(username="bob", is_staff=True)
        cls.non_staff = make_user(username="tom", is_staff=False)
        cls.url = reverse(viewname="user_create")
        cls.payload = {"username": "hironsan", "password1": "foobarbaz", "password2": "foobarbaz"}

    def test_staff_can_create_user(self):
        self.client.force_login(self.staff)
        response = self.client.post(self.url, data=self.payload)
        self.assertEqual(response.data["username"], "hironsan")

    def test_non_staff_cannot_create_user(self):
        self.client.force_login(self.non_staff)
        response = self.client.post(self.url, data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
