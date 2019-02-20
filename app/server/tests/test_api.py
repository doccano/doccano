from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from ..models import User, Project


class TestProjectListAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        cls.project_member = User.objects.create_user(username=cls.project_member_name,
                                                      password=cls.project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        cls.main_project = mixer.blend('server.Project')
        cls.main_project.users.add(cls.project_member)
        cls.main_project.users.add(super_user)
        sub_project = mixer.blend('server.Project')
        cls.url = reverse(viewname='project_list')
        cls.post_data = {'name': 'example', 'project_type': 'Seq2seq',
                         'description': 'example', 'guideline': 'example'}

    def test_returns_projects_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_return_projects_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data, [])

    def test_do_not_return_other_projects(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), self.project_member.projects.count())

    def test_allows_superuser_to_create_project(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.post(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_disallows_project_member_to_create_project(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.post(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestProjectDetailAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        cls.project_member = User.objects.create_user(username=cls.project_member_name,
                                                      password=cls.project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        cls.main_project = mixer.blend('server.Project')
        cls.main_project.users.add(cls.project_member)
        cls.main_project.users.add(super_user)
        sub_project = mixer.blend('server.Project')
        cls.url = reverse(viewname='project_detail', args=[cls.main_project.id])
        cls.post_data = {'name': 'example', 'project_type': 'Seq2seq',
                         'description': 'example', 'guideline': 'example'}

    def test_returns_project_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['id'], self.main_project.id)

    def test_do_not_return_project_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_superuser_to_update_project(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.patch(self.url, format='json', data={'description': 'lorem'})
        self.assertEqual(response.data['description'], 'lorem')

    def test_disallows_project_member_to_update_project(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.put(self.url, format='json', data={'description': 'lorem'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_superuser_to_delete_project(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_disallows_project_member_to_delete_project(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestLabelListAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        cls.main_project = mixer.blend('server.Project')
        cls.main_project.users.add(project_member)
        cls.main_project.users.add(super_user)
        mixer.blend('server.Label', project=cls.main_project)
        sub_project = mixer.blend('server.Project')
        mixer.blend('server.Label', project=sub_project)
        cls.url = reverse(viewname='label_list', args=[cls.main_project.id])
        cls.post_data = {'text': 'example'}

    def test_returns_labels_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_return_labels_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_do_not_return_labels_of_other_projects(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), self.main_project.labels.count())

    def test_allows_superuser_to_create_label(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.post(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_disallows_project_member_to_create_label(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.post(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestLabelDetailAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        cls.label = mixer.blend('server.Label')
        project = mixer.blend('server.Project')
        project.labels.add(cls.label)
        project.users.add(project_member)
        project.users.add(super_user)
        cls.url = reverse(viewname='label_detail', args=[project.id, cls.label.id])

    def test_returns_label_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['id'], self.label.id)

    def test_do_not_return_label_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_superuser_to_update_label(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.patch(self.url, format='json', data={'text': 'example'})
        self.assertEqual(response.data['text'], 'example')

    def test_disallows_project_member_to_update_label(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.put(self.url, format='json', data={'text': 'example'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_superuser_to_delete_label(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_disallows_project_member_to_delete_label(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDocumentListAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        cls.main_project = mixer.blend('server.Project')
        cls.main_project.users.add(project_member)
        cls.main_project.users.add(super_user)
        mixer.blend('server.Document', project=cls.main_project)
        sub_project = mixer.blend('server.Project')
        mixer.blend('server.Document', project=sub_project)
        cls.url = reverse(viewname='doc_list', args=[cls.main_project.id])
        cls.post_data = {'text': 'example'}

    def test_returns_docs_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_return_docs_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_do_not_return_docs_of_other_projects(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['count'], self.main_project.documents.count())

    def test_allows_superuser_to_create_doc(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.post(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_disallows_project_member_to_create_doc(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.post(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDocumentDetailAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        cls.doc = mixer.blend('server.Document')
        project = mixer.blend('server.Project')
        project.documents.add(cls.doc)
        project.users.add(project_member)
        project.users.add(super_user)
        cls.url = reverse(viewname='doc_detail', args=[project.id, cls.doc.id])

    def test_returns_doc_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['id'], self.doc.id)

    def test_do_not_return_doc_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_superuser_to_update_doc(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.patch(self.url, format='json', data={'text': 'example'})
        self.assertEqual(response.data['text'], 'example')

    def test_disallows_project_member_to_update_doc(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.put(self.url, format='json', data={'text': 'example'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_superuser_to_delete_doc(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_disallows_project_member_to_delete_doc(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.delete(self.url, format='json')
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
