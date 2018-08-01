from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from ..models import *


class TestAnnotationAPI(APITestCase):
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

    def create_label(self):
        label = mixer.blend('server.Label')

        return label

    def create_doc(self):
        doc = mixer.blend('server.Document')

        return doc

    def create_annotation(self):
        annotation = mixer.blend('server.DocumentAnnotation')

        return annotation

    def test_get_own_annotation(self):
        """
        Ensure we can get own annotation objects.
        """
        user = self.create_user()
        project = self.create_project()
        project.project_type = Project.DOCUMENT_CLASSIFICATION
        annotation = self.create_annotation()
        annotation.user = user
        project.users.add(user)
        project.documents.add(annotation.document)
        project.save()
        annotation.save()
        url = reverse('annotations', args=[project.id, annotation.document.id])

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data[0]['id'], annotation.id)

    def test_get_others_annotation(self):
        """
        Ensure we cannot get others annotation objects.
        """
        user = self.create_user()
        project = self.create_project()
        project.project_type = Project.DOCUMENT_CLASSIFICATION
        annotation = self.create_annotation()
        project.users.add(annotation.user)
        project.documents.add(annotation.document)
        project.save()
        annotation.save()
        url = reverse('annotations', args=[project.id, annotation.document.id])

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_annotation(self):
        """
        Ensure we can create a new annotation object.
        """
        user = self.create_user()
        project = self.create_project()
        doc = self.create_doc()
        label = self.create_label()
        project.project_type = Project.DOCUMENT_CLASSIFICATION
        project.users.add(user)
        project.documents.add(doc)
        project.labels.add(label)

        data = {'label_id': label.id}
        url = reverse('annotations', args=[project.id, doc.id])
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DocumentAnnotation.objects.count(), 1)

    def test_delete_annotation(self):
        """
        Ensure we cannot create a new project object by user.
        """
        user = self.create_user()
        project = self.create_project()
        project.project_type = Project.DOCUMENT_CLASSIFICATION
        annotation = self.create_annotation()
        annotation.user = user
        project.users.add(annotation.user)
        project.documents.add(annotation.document)
        project.save()
        annotation.save()

        url = reverse('ann', args=[project.id, annotation.document.id, annotation.id])
        self.assertEqual(DocumentAnnotation.objects.count(), 1)
        self.client.login(username=self.username, password=self.password)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DocumentAnnotation.objects.count(), 0)
