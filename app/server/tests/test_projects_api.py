from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from ..models import User, Project


class TestProjects(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.username = 'user'
        cls.password = 'pass'
        cls.super_username = 'super'
        cls.normal_user = User.objects.create_user(username=cls.username, password=cls.password)
        cls.super_user = User.objects.create_superuser(username=cls.super_username,
                                                       password=cls.password, email='fizz@buzz.com')
        cls.project1 = mixer.blend('server.Project', project_type=Project.DOCUMENT_CLASSIFICATION,
                                   users=[cls.normal_user, cls.super_user])
        cls.project2 = mixer.blend('server.Project', project_type=Project.DOCUMENT_CLASSIFICATION,
                                   users=[cls.super_user])
        cls.url = reverse('project-list')

    def setUp(self):
        self.client.login(username=self.username, password=self.password)

    def test_get_projects(self):
        """
        Ensure user can get project.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.project1.id)

    def test_get_progress(self):
        """
        Ensure user can get project's progress.
        """
        url = '{}{}/progress/'.format(self.url, self.project1.id)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)
        self.assertIn('remaining', response.data)
        self.assertIsInstance(response.data['total'], int)
        self.assertIsInstance(response.data['remaining'], int)

    def test_superuser_can_delete_project(self):
        """
        Ensure superuser can delete a project.
        """
        self.assertEqual(Project.objects.count(), 2)
        self.client.login(username=self.super_username, password=self.password)
        url = '{}{}/'.format(self.url, self.project2.id)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 1)

    def test_normal_user_cannot_delete_project(self):
        """
        Ensure normal user cannot delete a project.
        """
        self.assertEqual(Project.objects.count(), 2)
        url = '{}{}/'.format(self.url, self.project2.id)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 2)
