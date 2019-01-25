from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from ..models import User, Project


class TestAnnotationAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.username = 'user'
        cls.password = 'pass'
        cls.user1 = User.objects.create_user(username=cls.username, password=cls.password)
        cls.user2 = User.objects.create_user(username='user2', password='pass2')
        cls.project1 = mixer.blend('server.Project', project_type=Project.DOCUMENT_CLASSIFICATION,
                                   users=[cls.user1, cls.user2])
        cls.project2 = mixer.blend('server.Project', project_type=Project.DOCUMENT_CLASSIFICATION,
                                   users=[cls.user2])
        cls.doc1 = mixer.blend('server.Document', project=cls.project1)
        cls.doc2 = mixer.blend('server.Document', project=cls.project1)
        cls.label = mixer.blend('server.Label', project=cls.project1)
        cls.annotation1 = mixer.blend('server.DocumentAnnotation', document=cls.doc1, user=cls.user1)
        cls.annotation2 = mixer.blend('server.DocumentAnnotation', document=cls.doc1, user=cls.user2)

    def setUp(self):
        self.client.login(username=self.username, password=self.password)

    def test_fetch_own_annotation(self):
        """
        Ensure user can fetch only own annotation.
        """
        url = reverse('annotations', args=[self.project1.id, self.doc1.id])
        r = self.client.get(url, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)
        self.assertEqual(r.data[0]['id'], self.annotation1.id)

    def test_fetch_other_projects_annotation(self):
        """
        Ensure user cannot fetch other project's annotation.
        """
        url = reverse('annotations', args=[self.project2.id, self.doc1.id])
        r = self.client.get(url, format='json')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_annotate_doc(self):
        """
        Ensure user can annotate a document.
        """
        # Try to annotate a empty document(doc2).
        data = {'label': self.label.id}
        url = reverse('annotations', args=[self.project1.id, self.doc2.id])
        r = self.client.post(url, data, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(self.doc2.doc_annotations.all()), 1)

    def test_delete_annotation(self):
        """
        Ensure user can delete only own annotation.
        """
        self.assertEqual(len(self.doc1.doc_annotations.all()), 2)

        # Try to delete own annotation.
        url = reverse('ann', args=[self.project1.id, self.doc1.id, self.annotation1.id])
        r = self.client.delete(url, format='json')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(self.doc1.doc_annotations.all()), 1)

        # Try to delete other's annotation.
        url = reverse('ann', args=[self.project1.id, self.doc1.id, self.annotation2.id])
        r = self.client.delete(url, format='json')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
