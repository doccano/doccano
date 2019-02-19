from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from ..models import User, Project, Label


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
        user = self.create_user()  # noqa: F841
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
        user = self.create_user()  # noqa: F841
        project = self.create_project()
        doc = self.create_doc()
        project.documents.add(doc)
        url = reverse('docs', args=[project.id])

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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
