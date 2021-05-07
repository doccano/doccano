from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import DOCUMENT_CLASSIFICATION
from .utils import (create_default_roles, make_project, make_user,
                    remove_all_role_mappings)


class TestProjectList(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = make_project(
            task=DOCUMENT_CLASSIFICATION,
            users=['admin'],
            roles=[settings.ROLE_PROJECT_ADMIN]
        )
        cls.non_member = make_user(username='bob')
        cls.url = reverse(viewname='project_list')

    def test_return_projects_to_member(self):
        self.client.force_login(self.project.users[0])
        response = self.client.get(self.url)
        project = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(project['id'], self.project.item.id)

    def test_does_not_return_project_to_non_member(self):
        self.client.force_login(self.non_member)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 0)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


class TestProjectCreate(APITestCase):

    @classmethod
    def setUpTestData(cls):
        create_default_roles()
        cls.user = make_user(username='bob')
        cls.url = reverse(viewname='project_list')
        cls.data = {
            'name': 'example',
            'project_type': 'DocumentClassification',
            'description': 'example',
            'guideline': 'example',
            'resourcetype': 'TextClassificationProject'
        }

    def test_allow_authenticated_user_to_create_project(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.data['name'])

    def test_disallow_unauthenticated_user_to_create_project(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


class TestProjectDetailAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = make_project(
            task=DOCUMENT_CLASSIFICATION,
            users=['admin', 'approver', 'annotator'],
            roles=[
                settings.ROLE_PROJECT_ADMIN,
                settings.ROLE_ANNOTATION_APPROVER,
                settings.ROLE_ANNOTATOR,
            ]
        )
        cls.non_member = make_user(username='bob')
        cls.url = reverse(viewname='project_detail', args=[cls.project.item.id])
        cls.data = {'description': 'lorem'}

    def test_return_project_to_member(self):
        for member in self.project.users:
            self.client.force_login(member)
            response = self.client.get(self.url)
            self.assertEqual(response.data['id'], self.project.item.id)

    def test_does_not_return_project_to_non_member(self):
        self.client.force_login(self.non_member)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_admin_to_update_project(self):
        self.client.force_login(self.project.users[0])
        response = self.client.patch(self.url, data=self.data)
        self.assertEqual(response.data['description'], self.data['description'])

    def test_disallows_non_admin_to_update_project(self):
        for member in self.project.users[1:]:
            self.client.force_login(member)
            response = self.client.patch(self.url, data=self.data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallows_non_member_to_update_project(self):
        self.client.force_login(self.non_member)
        response = self.client.patch(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_admin_to_delete_project(self):
        self.client.force_login(self.project.users[0])
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_disallows_non_admin_to_delete_project(self):
        for member in self.project.users[1:]:
            self.client.force_login(member)
            response = self.client.delete(self.url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallows_non_member_to_delete_project(self):
        self.client.force_login(self.non_member)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()
