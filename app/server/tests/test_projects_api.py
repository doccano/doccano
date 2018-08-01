from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from ..models import *


class TestProjects(APITestCase):

    def setUp(self):
        self.username, self.password = 'user', 'pass'
        self.url = reverse('project-list')

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

    def add_user_to_project(self, user, project):
        project.users.add(user)

    def test_get_projects(self):
        """
        Ensure we can get project objects.
        """
        user = self.create_user()
        project = self.create_project()
        self.add_user_to_project(user, project)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url, format='json')
        p = response.data[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(p['id'], project.id)
        self.assertEqual(p['name'], project.name)
        self.assertEqual(p['description'], project.description)
        self.assertEqual(p['project_type'], project.project_type)
        self.assertEqual(p['image'], project.image)

    def test_get_progress(self):
        """
        Ensure we can get project's progress.
        """
        user = self.create_user()
        project = self.create_project()
        self.add_user_to_project(user, project)

        url = '{}{}/progress/'.format(self.url, project.id)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)
        self.assertIn('remaining', response.data)
        self.assertIsInstance(response.data['total'], int)
        self.assertIsInstance(response.data['remaining'], int)

    def test_create_project_by_admin(self):
        """
        Ensure we can create a new project object by admin.
        """
        user = self.create_superuser()
        data = {'name': 'DabApps',
                'description': 'desc',
                'project_type': Project.DOCUMENT_CLASSIFICATION,
                'users': [user.id]}
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().name, 'DabApps')

    def test_create_project_by_user(self):
        """
        Ensure we cannot create a new project object by user.
        """
        user = self.create_user()
        data = {'name': 'DabApps',
                'description': 'desc',
                'project_type': Project.DOCUMENT_CLASSIFICATION,
                'users': [user.id]}
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_project_by_superuser(self):
        """
        Ensure we can delete a project by superuser.
        """
        user = self.create_superuser()
        project = self.create_project()
        self.assertEqual(Project.objects.count(), 1)
        self.client.login(username=self.username, password=self.password)
        url = '{}{}/'.format(self.url, project.id)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)

    def test_delete_project_by_user(self):
        """
        Ensure we cannot delete a project by user.
        """
        user = self.create_user()
        project = self.create_project()
        self.assertEqual(Project.objects.count(), 1)
        self.client.login(username=self.username, password=self.password)
        url = '{}{}/'.format(self.url, project.id)
        response = self.client.delete(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)
