import os

from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .utils import (DATA_DIR, make_label, make_project, make_user,
                    prepare_project)


class TestLabelList(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.non_member = make_user(username='bob')
        cls.project_a = prepare_project()
        cls.label = make_label(cls.project_a.item)
        cls.url = reverse(viewname='label_list', args=[cls.project_a.item.id])

        # Ensure that the API does not return the labels of the other project.
        cls.project_b = make_project(
            task='Any',
            users=['admin'],
            roles=[settings.ROLE_PROJECT_ADMIN]
        )
        make_label(cls.project_b.item)

    def test_returns_labels_to_project_member(self):
        for member in self.project_a.users:
            self.client.force_login(member)
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['id'], self.label.id)

    def test_does_not_return_labels_to_non_project_member(self):
        self.client.force_login(self.non_member)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_does_not_return_labels_to_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestLabelCreate(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.non_member = make_user(username='bob')
        cls.project = prepare_project()
        cls.url = reverse(viewname='label_list', args=[cls.project.item.id])
        cls.data = {'text': 'example'}

    def assert_create_label(self, user=None, expected_status=status.HTTP_403_FORBIDDEN):
        if user:
            self.client.force_login(user)
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, expected_status)

    def test_allows_admin_to_create_label(self):
        self.assert_create_label(self.project.users[0], status.HTTP_201_CREATED)

    def test_disallows_non_admin_to_create_label(self):
        for member in self.project.users[1:]:
            self.assert_create_label(member, status.HTTP_403_FORBIDDEN)

    def test_disallows_non_project_member_to_create_label(self):
        self.assert_create_label(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_disallows_unauthenticated_user_to_create_label(self):
        self.assert_create_label(expected_status=status.HTTP_403_FORBIDDEN)


class TestLabelDetailAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.non_member = make_user(username='bob')
        cls.project = prepare_project()
        cls.label = make_label(cls.project.item)
        cls.url = reverse(viewname='label_detail', args=[cls.project.item.id, cls.label.id])
        cls.data = {'text': 'example'}

    def test_returns_label_to_project_member(self):
        for member in self.project.users:
            self.client.force_login(member)
            response = self.client.get(self.url)
            self.assertEqual(response.data['id'], self.label.id)

    def test_does_not_return_label_to_non_project_member(self):
        self.client.force_login(self.non_member)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_does_not_return_label_to_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def assert_update_label(self, user=None, expected_status=status.HTTP_403_FORBIDDEN):
        if user:
            self.client.force_login(user)
        response = self.client.patch(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, expected_status)
        return response

    def test_allows_admin_to_update_label(self):
        response = self.assert_update_label(
            user=self.project.users[0],
            expected_status=status.HTTP_200_OK
        )
        self.assertEqual(response.data['text'], self.data['text'])

    def test_disallows_non_admin_to_update_label(self):
        for member in self.project.users[1:]:
            self.assert_update_label(member, status.HTTP_403_FORBIDDEN)

    def test_disallows_non_project_member_to_update_label(self):
        self.assert_update_label(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_disallows_unauthenticated_user_to_update_label(self):
        self.assert_update_label(expected_status=status.HTTP_403_FORBIDDEN)

    def assert_delete_label(self, user=None, expected_status=status.HTTP_403_FORBIDDEN):
        if user:
            self.client.force_login(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, expected_status)

    def test_allows_admin_to_delete_label(self):
        self.assert_delete_label(self.project.users[0], status.HTTP_204_NO_CONTENT)

    def test_disallows_non_admin_to_delete_label(self):
        for member in self.project.users[1:]:
            self.assert_delete_label(member, status.HTTP_403_FORBIDDEN)

    def test_disallows_non_project_member_to_delete_label(self):
        self.assert_delete_label(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_disallows_unauthenticated_user_to_delete_label(self):
        self.assert_delete_label(expected_status=status.HTTP_403_FORBIDDEN)


class TestLabelUploadAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.non_member = make_user(username='bob')
        cls.project = prepare_project()
        cls.url = reverse(viewname='label_upload', args=[cls.project.item.id])

    def assert_upload_file(self, filename, user=None, expected_status=status.HTTP_403_FORBIDDEN):
        if user:
            self.client.force_login(user)
        with open(os.path.join(DATA_DIR, filename), 'rb') as f:
            response = self.client.post(self.url, data={'file': f})
        self.assertEqual(response.status_code, expected_status)

    def test_allows_project_admin_to_upload_label(self):
        self.assert_upload_file('valid_labels.json', self.project.users[0], status.HTTP_201_CREATED)

    def test_disallows_project_member_to_upload_label(self):
        for member in self.project.users[1:]:
            self.assert_upload_file('valid_labels.json', member, status.HTTP_403_FORBIDDEN)

    def test_disallows_non_project_member_to_upload_label(self):
        self.assert_upload_file('valid_labels.json', self.non_member, status.HTTP_403_FORBIDDEN)

    def test_disallows_unauthenticated_user_to_upload_label(self):
        self.assert_upload_file('valid_labels.json', expected_status=status.HTTP_403_FORBIDDEN)

    def test_try_to_upload_invalid_file(self):
        self.assert_upload_file('invalid_labels.json', self.project.users[0], status.HTTP_400_BAD_REQUEST)
