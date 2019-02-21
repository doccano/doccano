from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from ..models import User, SequenceAnnotation


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


class TestEntityListAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)
        label = mixer.blend('server.Label')

        cls.main_project = mixer.blend('server.Project')
        cls.main_project.users.add(project_member)
        cls.main_project.labels.add(label)
        main_project_doc = mixer.blend('server.Document', project=cls.main_project)
        mixer.blend('server.SequenceAnnotation', document=main_project_doc)

        sub_project = mixer.blend('server.Project')
        sub_project_doc = mixer.blend('server.Document', project=sub_project)
        mixer.blend('server.SequenceAnnotation', document=sub_project_doc)

        cls.url = reverse(viewname='entity_list', args=[cls.main_project.id, main_project_doc.id])
        cls.post_data = {'start_offset': 0, 'end_offset': 1, 'label': label.id}
        cls.count = SequenceAnnotation.objects.filter(document=main_project_doc).count()

    def test_returns_entities_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_return_entities_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_do_not_return_entities_of_other_projects(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), self.count)

    def test_allows_project_member_to_create_entity(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.post(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_disallows_non_project_member_to_create_entity(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.post(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestEntityDetailAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)
        label = mixer.blend('server.Label')

        cls.main_project = mixer.blend('server.Project')
        cls.main_project.users.add(project_member)
        cls.main_project.labels.add(label)
        main_project_doc = mixer.blend('server.Document', project=cls.main_project)
        main_project_entity = mixer.blend('server.SequenceAnnotation', document=main_project_doc)

        sub_project = mixer.blend('server.Project')
        sub_project_doc = mixer.blend('server.Document', project=sub_project)
        mixer.blend('server.SequenceAnnotation', document=sub_project_doc)

        cls.url = reverse(viewname='entity_detail', args=[cls.main_project.id,
                                                          main_project_doc.id,
                                                          main_project_entity.id])
        cls.post_data = {'start_offset': 0, 'end_offset': 10}
        cls.count = SequenceAnnotation.objects.filter(document=main_project_doc).count()

    def test_returns_entity_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_return_entity_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_project_member_to_update_entity(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_disallows_non_project_member_to_update_entity(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.put(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_project_member_to_delete_entity(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_disallows_project_member_to_delete_entity(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
