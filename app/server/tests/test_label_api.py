from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from ..models import *


class TestLabelAPI(APITestCase):
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

    def add_user_to_project(self, user, project):
        project.users.add(user)

    def create_label(self):
        label = mixer.blend('server.Label')

        return label

    def test_get_labels_by_project_user(self):
        """
        Ensure we can get label objects by project user.
        """
        user = self.create_user()
        project = self.create_project()
        self.add_user_to_project(user, project)
        label = self.create_label()
        project.labels.add(label)
        url = reverse('labels', args=[project.id])

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url, format='json')
        r = response.data[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(r['id'], label.id)

    def test_get_labels_by_other(self):
        """
        Ensure we cannot get label objects by other.
        """
        user = self.create_user()
        project = self.create_project()
        label = self.create_label()
        project.labels.add(label)
        url = reverse('labels', args=[project.id])

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_label_by_admin(self):
        """
        Ensure we can create a new project object by admin.
        """
        user = self.create_superuser()
        project = self.create_project()
        self.add_user_to_project(user, project)
        data = {'text': 'label1',
                'shortcut': 'a',
                'background_color': '#ffffff',
                'text_color': '#ffffff'}
        url = reverse('labels', args=[project.id])
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(Label.objects.get().text, 'label1')

    def test_create_label_by_user(self):
        """
        Ensure we cannot create a new project object by user.
        """
        user = self.create_user()
        project = self.create_project()
        self.add_user_to_project(user, project)
        data = {'text': 'label1',
                'shortcut': 'a',
                'background_color': '#ffffff',
                'text_color': '#ffffff'}
        url = reverse('labels', args=[project.id])
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_label_by_admin(self):
        """
        Ensure we can delete a label by superuser.
        """
        user = self.create_superuser()
        project = self.create_project()
        label = self.create_label()
        self.add_user_to_project(user, project)
        project.labels.add(label)
        self.assertEqual(Label.objects.count(), 1)
        self.client.login(username=self.username, password=self.password)
        url = reverse('label', args=[project.id, label.id])
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Label.objects.count(), 0)

    def test_delete_label_by_user(self):
        """
        Ensure we cannot delete a label by user.
        """
        user = self.create_user()
        project = self.create_project()
        label = self.create_label()
        self.add_user_to_project(user, project)
        project.labels.add(label)
        self.assertEqual(Label.objects.count(), 1)
        self.client.login(username=self.username, password=self.password)
        url = reverse('label', args=[project.id, label.id])
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Label.objects.count(), 1)
