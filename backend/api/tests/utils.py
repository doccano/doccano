from typing import Any, Dict

from rest_framework import status
from rest_framework.test import APITestCase


class CRUDMixin(APITestCase):
    url = ""
    data: Dict[str, Any] = {}

    def assert_fetch(self, user=None, expected=status.HTTP_403_FORBIDDEN):
        if user:
            self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, expected)
        return response

    def assert_create(self, user=None, expected=status.HTTP_403_FORBIDDEN):
        if user:
            self.client.force_login(user)
        response = self.client.post(self.url, data=self.data, format="json")
        self.assertEqual(response.status_code, expected)
        return response

    def assert_update(self, user=None, expected=status.HTTP_403_FORBIDDEN):
        if user:
            self.client.force_login(user)
        response = self.client.patch(self.url, data=self.data, format="json")
        self.assertEqual(response.status_code, expected)
        return response

    def assert_delete(self, user=None, expected=status.HTTP_403_FORBIDDEN, data=None):
        if user:
            self.client.force_login(user)

        if data is None:
            data = {}
        response = self.client.delete(self.url, data=data)
        self.assertEqual(response.status_code, expected)
