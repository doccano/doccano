from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mixer.backend.django import mixer


class TestProjects(APITestCase):

    def setUp(self):
        user = mixer.blend('auth.User')
        self.project = mixer.blend('server.Project')
        self.project.users.add(user)
        self.client.force_login(user=user)

    def test_get_projects(self):
        """
        Ensure we can get project objects.
        """
        url = reverse('project-list')
        response = self.client.get(url, format='json')
        project = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(project['id'], self.project.id)
        self.assertEqual(project['name'], self.project.name)
        self.assertEqual(project['description'], self.project.description)
        self.assertEqual(project['project_type'], self.project.project_type)
        self.assertEqual(project['image'], self.project.image)
