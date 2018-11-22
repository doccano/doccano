from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from ..models import *


class TestDocAPI(APITestCase):
    def setUp(self):
        self.username, self.password = 'user', 'pass'

    def create_user(self):
        user = User.objects.create_user(username=self.username, password=self.password)

        return user

    def create_superuser(self):
        user = User.objects.create_superuser(username=self.username,
                                             password=self.password,
                                             email='hoge@example.com')
        return user

    def create_project(self):
        project = mixer.blend('server.Project')

        return project

    def create_doc(self):
        doc = mixer.blend('server.Document')

        return doc

    def test_get_docs_by_project_user(self):
        """
        Ensure we can get document objects by project user.
        """
        user = self.create_user()
        project = self.create_project()
        project.users.add(user)
        doc = self.create_doc()
        project.documents.add(doc)
        url = reverse('docs', args=[project.id])

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], doc.id)

    def test_get_docs_by_other(self):
        """
        Ensure we cannot get label objects by other.
        """
        user = self.create_user()
        project = self.create_project()
        doc = self.create_doc()
        project.documents.add(doc)
        url = reverse('docs', args=[project.id])

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
