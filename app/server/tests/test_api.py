from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from ..models import User, SequenceAnnotation, Document


class TestProjectListAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.main_project_member_name = 'project_member_name'
        cls.main_project_member_pass = 'project_member_pass'
        cls.sub_project_member_name = 'sub_project_member_name'
        cls.sub_project_member_pass = 'sub_project_member_pass'
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        main_project_member = User.objects.create_user(username=cls.main_project_member_name,
                                                       password=cls.main_project_member_pass)
        sub_project_member = User.objects.create_user(username=cls.sub_project_member_name,
                                                      password=cls.sub_project_member_pass)
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')

        cls.main_project = mixer.blend('server.Project', users=[main_project_member])
        cls.sub_project = mixer.blend('server.Project', users=[sub_project_member])

        cls.url = reverse(viewname='project_list')
        cls.data = {'name': 'example', 'project_type': 'Seq2seq',
                    'description': 'example', 'guideline': 'example'}
        cls.num_project = main_project_member.projects.count()

    def test_returns_main_project_to_main_project_member(self):
        self.client.login(username=self.main_project_member_name,
                          password=self.main_project_member_pass)
        response = self.client.get(self.url, format='json')
        project = response.data[0]
        num_project = len(response.data)
        self.assertEqual(num_project, self.num_project)
        self.assertEqual(project['id'], self.main_project.id)

    def test_do_not_return_main_project_to_sub_project_member(self):
        self.client.login(username=self.sub_project_member_name,
                          password=self.sub_project_member_pass)
        response = self.client.get(self.url, format='json')
        project = response.data[0]
        num_project = len(response.data)
        self.assertEqual(num_project, self.num_project)
        self.assertNotEqual(project['id'], self.main_project.id)

    def test_allows_superuser_to_create_project(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.post(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_disallows_project_member_to_create_project(self):
        self.client.login(username=self.main_project_member_name,
                          password=self.main_project_member_pass)
        response = self.client.post(self.url, format='json', data=self.data)
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
        cls.main_project = mixer.blend('server.Project', users=[cls.project_member, super_user])
        sub_project = mixer.blend('server.Project', users=[non_project_member])
        cls.url = reverse(viewname='project_detail', args=[cls.main_project.id])
        cls.data = {'description': 'lorem'}

    def test_returns_main_project_detail_to_main_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['id'], self.main_project.id)

    def test_do_not_return_main_project_to_sub_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_superuser_to_update_project(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.patch(self.url, format='json', data=self.data)
        self.assertEqual(response.data['description'], self.data['description'])

    def test_disallows_project_member_to_update_project(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.data)
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
        cls.main_project = mixer.blend('server.Project', users=[project_member, super_user])
        cls.main_project_label = mixer.blend('server.Label', project=cls.main_project)

        sub_project = mixer.blend('server.Project', users=[non_project_member])
        mixer.blend('server.Label', project=sub_project)
        cls.url = reverse(viewname='label_list', args=[cls.main_project.id])
        cls.data = {'text': 'example'}

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
        label = response.data[0]
        num_labels = len(response.data)
        self.assertEqual(num_labels, len(self.main_project.labels.all()))
        self.assertEqual(label['id'], self.main_project_label.id)

    def test_allows_superuser_to_create_label(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.post(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_disallows_project_member_to_create_label(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.post(self.url, format='json', data=self.data)
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
        project = mixer.blend('server.Project', users=[project_member, super_user])
        cls.label = mixer.blend('server.Label', project=project)
        cls.url = reverse(viewname='label_detail', args=[project.id, cls.label.id])
        cls.data = {'text': 'example'}

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
        response = self.client.patch(self.url, format='json', data=self.data)
        self.assertEqual(response.data['text'], self.data['text'])

    def test_disallows_project_member_to_update_label(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.data)
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

        cls.main_project = mixer.blend('server.Project', users=[project_member, super_user])
        mixer.blend('server.Document', project=cls.main_project)

        sub_project = mixer.blend('server.Project', users=[non_project_member])
        mixer.blend('server.Document', project=sub_project)
        cls.url = reverse(viewname='doc_list', args=[cls.main_project.id])
        cls.data = {'text': 'example'}

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
        response = self.client.post(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_disallows_project_member_to_create_doc(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.post(self.url, format='json', data=self.data)
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
        project = mixer.blend('server.Project', users=[project_member, super_user])
        cls.doc = mixer.blend('server.Document', project=project)
        cls.url = reverse(viewname='doc_detail', args=[project.id, cls.doc.id])
        cls.data = {'text': 'example'}

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
        response = self.client.patch(self.url, format='json', data=self.data)
        self.assertEqual(response.data['text'], self.data['text'])

    def test_disallows_project_member_to_update_doc(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.data)
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
        cls.another_project_member_name = 'another_project_member_name'
        cls.another_project_member_pass = 'another_project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        another_project_member = User.objects.create_user(username=cls.another_project_member_name,
                                                          password=cls.another_project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)

        main_project = mixer.blend('server.Project', users=[project_member, another_project_member])
        main_project_label = mixer.blend('server.Label', project=main_project)
        main_project_doc = mixer.blend('server.Document', project=main_project)
        mixer.blend('server.SequenceAnnotation', document=main_project_doc, user=project_member)
        mixer.blend('server.SequenceAnnotation', document=main_project_doc, user=another_project_member)

        sub_project = mixer.blend('server.Project', users=[non_project_member])
        sub_project_doc = mixer.blend('server.Document', project=sub_project)
        mixer.blend('server.SequenceAnnotation', document=sub_project_doc)

        cls.url = reverse(viewname='entity_list', args=[main_project.id, main_project_doc.id])
        cls.post_data = {'start_offset': 0, 'end_offset': 1, 'label': main_project_label.id}
        cls.num_entity_of_project_member = SequenceAnnotation.objects.filter(document=main_project_doc,
                                                                             user=project_member).count()

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

    def test_do_not_return_entities_of_another_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), self.num_entity_of_project_member)

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
        cls.another_project_member_name = 'another_project_member_name'
        cls.another_project_member_pass = 'another_project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        another_project_member = User.objects.create_user(username=cls.another_project_member_name,
                                                          password=cls.another_project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)

        main_project = mixer.blend('server.Project', users=[project_member, another_project_member])
        main_project_doc = mixer.blend('server.Document', project=main_project)
        main_project_entity = mixer.blend('server.SequenceAnnotation',
                                          document=main_project_doc, user=project_member)
        another_entity = mixer.blend('server.SequenceAnnotation',
                                     document=main_project_doc, user=another_project_member)

        sub_project = mixer.blend('server.Project', users=[non_project_member])
        sub_project_doc = mixer.blend('server.Document', project=sub_project)
        mixer.blend('server.SequenceAnnotation', document=sub_project_doc)

        cls.url = reverse(viewname='entity_detail', args=[main_project.id,
                                                          main_project_doc.id,
                                                          main_project_entity.id])
        cls.another_url = reverse(viewname='entity_detail', args=[main_project.id,
                                                                  main_project_doc.id,
                                                                  another_entity.id])
        cls.post_data = {'start_offset': 0, 'end_offset': 10}

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

    def test_do_not_return_entity_by_another_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.another_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_project_member_to_update_entity(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_disallows_non_project_member_to_update_entity(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallows_project_member_to_update_entity_of_another_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.another_url, format='json', data=self.post_data)
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

    def test_disallows_project_member_to_delete_entity_of_another_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.delete(self.another_url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestSearch(APITestCase):

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

        cls.main_project = mixer.blend('server.Project', users=[project_member])
        cls.search_term = 'example'
        mixer.blend('server.Document', text=cls.search_term, project=cls.main_project)
        mixer.blend('server.Document', text='Lorem', project=cls.main_project)

        sub_project = mixer.blend('server.Project', users=[non_project_member])
        mixer.blend('server.Document', text=cls.search_term, project=sub_project)
        cls.url = reverse(viewname='doc_list', args=[cls.main_project.id])
        cls.data = {'q': cls.search_term}

    def test_can_filter_doc_by_term(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=self.data)
        count = Document.objects.filter(text__contains=self.search_term,
                                        project=self.main_project).count()
        self.assertEqual(response.data['count'], count)

    def test_can_order_doc_by_created_at_ascending(self):
        params = {'ordering': 'created_at'}
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=params)
        docs = Document.objects.filter(project=self.main_project).order_by('created_at').values()
        for d1, d2 in zip(response.data['results'], docs):
            self.assertEqual(d1['id'], d2['id'])

    def test_can_order_doc_by_created_at_descending(self):
        params = {'ordering': '-created_at'}
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=params)
        docs = Document.objects.filter(project=self.main_project).order_by('-created_at').values()
        for d1, d2 in zip(response.data['results'], docs):
            self.assertEqual(d1['id'], d2['id'])


class TestFilter(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        cls.main_project = mixer.blend('server.Project', users=[project_member])
        cls.label1 = mixer.blend('server.Label', project=cls.main_project)
        cls.label2 = mixer.blend('server.Label', project=cls.main_project)
        doc1 = mixer.blend('server.Document', project=cls.main_project)
        doc2 = mixer.blend('server.Document', project=cls.main_project)
        mixer.blend('server.SequenceAnnotation', document=doc1, user=project_member, label=cls.label1)
        mixer.blend('server.SequenceAnnotation', document=doc2, user=project_member, label=cls.label2)
        cls.url = reverse(viewname='doc_list', args=[cls.main_project.id])
        cls.params = {'seq_annotations__label__id': cls.label1.id}

    def test_can_filter_by_label(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=self.params)
        docs = Document.objects.filter(project=self.main_project,
                                       seq_annotations__label__id=self.label1.id).values()
        for d1, d2 in zip(response.data['results'], docs):
            self.assertEqual(d1['id'], d2['id'])
