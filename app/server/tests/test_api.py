import os

from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from model_mommy import mommy
from ..models import User, SequenceAnnotation, Document
from ..models import DOCUMENT_CLASSIFICATION, SEQUENCE_LABELING, SEQ2SEQ
from ..utils import PlainTextParser, CoNLLParser, JSONParser, CSVParser
from ..exceptions import FileParseException
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
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

        cls.main_project = mommy.make('server.TextClassificationProject', users=[main_project_member])
        cls.sub_project = mommy.make('server.TextClassificationProject', users=[sub_project_member])

        cls.url = reverse(viewname='project_list')
        cls.data = {'name': 'example', 'project_type': 'DocumentClassification',
                    'description': 'example', 'guideline': 'example',
                    'resourcetype': 'TextClassificationProject'}
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


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
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
        cls.main_project = mommy.make('server.TextClassificationProject', users=[cls.project_member, super_user])
        sub_project = mommy.make('server.TextClassificationProject', users=[non_project_member])
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
        cls.main_project = mommy.make('server.Project', users=[project_member, super_user])
        cls.main_project_label = mommy.make('server.Label', project=cls.main_project)

        sub_project = mommy.make('server.Project', users=[non_project_member])
        other_project = mommy.make('server.Project', users=[super_user])
        mommy.make('server.Label', project=sub_project)
        cls.url = reverse(viewname='label_list', args=[cls.main_project.id])
        cls.other_url = reverse(viewname='label_list', args=[other_project.id])
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

    def test_can_create_multiple_labels_without_shortcut_key(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        labels = [
            {'text': 'Ruby', 'prefix_key': None, 'suffix_key': None},
            {'text': 'PHP', 'prefix_key': None, 'suffix_key': None}
        ]
        for label in labels:
            response = self.client.post(self.url, format='json', data=label)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_same_label_in_multiple_projects(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        label = {'text': 'LOC', 'prefix_key': None, 'suffix_key': 'l'}
        response = self.client.post(self.url, format='json', data=label)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.other_url, format='json', data=label)
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
        project = mommy.make('server.Project', users=[project_member, super_user])
        cls.label = mommy.make('server.Label', project=project)
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

        cls.main_project = mommy.make('server.TextClassificationProject', users=[project_member, super_user])
        mommy.make('server.Document', project=cls.main_project)

        cls.random_order_project = mommy.make('server.TextClassificationProject', users=[project_member, super_user],
                                              randomize_document_order=True)
        mommy.make('server.Document', 100, project=cls.random_order_project)

        sub_project = mommy.make('server.TextClassificationProject', users=[non_project_member])
        mommy.make('server.Document', project=sub_project)
        cls.url = reverse(viewname='doc_list', args=[cls.main_project.id])
        cls.random_order_project_url = reverse(viewname='doc_list', args=[cls.random_order_project.id])
        cls.data = {'text': 'example'}

    def test_returns_docs_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_docs_in_consistent_order_for_all_users(self):
        self.client.login(username=self.project_member_name, password=self.project_member_pass)
        user1_documents = self.client.get(self.url, format='json').json().get('results')
        self.client.logout()

        self.client.login(username=self.super_user_name, password=self.super_user_pass)
        user2_documents = self.client.get(self.url, format='json').json().get('results')
        self.client.logout()

        self.assertEqual(user1_documents, user2_documents)

    def test_can_return_docs_in_consistent_random_order(self):
        self.client.login(username=self.project_member_name, password=self.project_member_pass)
        user1_documents1 = self.client.get(self.random_order_project_url, format='json').json().get('results')
        user1_documents2 = self.client.get(self.random_order_project_url, format='json').json().get('results')
        self.client.logout()
        self.assertEqual(user1_documents1, user1_documents2)

        self.client.login(username=self.super_user_name, password=self.super_user_pass)
        user2_documents1 = self.client.get(self.random_order_project_url, format='json').json().get('results')
        user2_documents2 = self.client.get(self.random_order_project_url, format='json').json().get('results')
        self.client.logout()
        self.assertEqual(user2_documents1, user2_documents2)

        self.assertNotEqual(user1_documents1, user2_documents1)
        self.assertNotEqual(user1_documents2, user2_documents2)

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
        project = mommy.make('server.TextClassificationProject', users=[project_member, super_user])
        cls.doc = mommy.make('server.Document', project=project)
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


class TestAnnotationListAPI(APITestCase):

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

        main_project = mommy.make('server.SequenceLabelingProject', users=[project_member, another_project_member])
        main_project_label = mommy.make('server.Label', project=main_project)
        main_project_doc = mommy.make('server.Document', project=main_project)
        mommy.make('server.SequenceAnnotation', document=main_project_doc, user=project_member)
        mommy.make('server.SequenceAnnotation', document=main_project_doc, user=another_project_member)

        sub_project = mommy.make('server.SequenceLabelingProject', users=[non_project_member])
        sub_project_doc = mommy.make('server.Document', project=sub_project)
        mommy.make('server.SequenceAnnotation', document=sub_project_doc)

        cls.url = reverse(viewname='annotation_list', args=[main_project.id, main_project_doc.id])
        cls.post_data = {'start_offset': 0, 'end_offset': 1, 'label': main_project_label.id}
        cls.num_entity_of_project_member = SequenceAnnotation.objects.filter(document=main_project_doc,
                                                                             user=project_member).count()

    def test_returns_annotations_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_return_annotations_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_do_not_return_annotations_of_another_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), self.num_entity_of_project_member)

    def test_allows_project_member_to_create_annotation(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.post(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_disallows_non_project_member_to_create_annotation(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.post(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAnnotationDetailAPI(APITestCase):

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

        main_project = mommy.make('server.SequenceLabelingProject',
                                  users=[project_member, another_project_member])
        main_project_doc = mommy.make('server.Document', project=main_project)
        main_project_entity = mommy.make('server.SequenceAnnotation',
                                         document=main_project_doc, user=project_member)
        another_entity = mommy.make('server.SequenceAnnotation',
                                    document=main_project_doc, user=another_project_member)

        sub_project = mommy.make('server.SequenceLabelingProject', users=[non_project_member])
        sub_project_doc = mommy.make('server.Document', project=sub_project)
        mommy.make('server.SequenceAnnotation', document=sub_project_doc)

        cls.url = reverse(viewname='annotation_detail', args=[main_project.id,
                                                              main_project_doc.id,
                                                              main_project_entity.id])
        cls.another_url = reverse(viewname='annotation_detail', args=[main_project.id,
                                                                      main_project_doc.id,
                                                                      another_entity.id])
        cls.post_data = {'start_offset': 0, 'end_offset': 10}

    def test_returns_annotation_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_return_annotation_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_do_not_return_annotation_by_another_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.another_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_project_member_to_update_annotation(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_disallows_non_project_member_to_update_annotation(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallows_project_member_to_update_annotation_of_another_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.another_url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_project_member_to_delete_annotation(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_disallows_project_member_to_delete_annotation(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallows_project_member_to_delete_annotation_of_another_member(self):
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

        cls.main_project = mommy.make('server.TextClassificationProject', users=[project_member])
        cls.search_term = 'example'
        doc1 = mommy.make('server.Document', text=cls.search_term, project=cls.main_project)
        doc2 = mommy.make('server.Document', text='Lorem', project=cls.main_project)
        label1 = mommy.make('server.Label', project=cls.main_project)
        label2 = mommy.make('server.Label', project=cls.main_project)
        mommy.make('server.SequenceAnnotation', document=doc1, user=project_member, label=label1)
        mommy.make('server.SequenceAnnotation', document=doc2, user=project_member, label=label2)

        sub_project = mommy.make('server.TextClassificationProject', users=[non_project_member])
        mommy.make('server.Document', text=cls.search_term, project=sub_project)
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

    def test_can_order_doc_by_annotation_updated_at_ascending(self):
        params = {'ordering': 'seq_annotations__updated_at'}
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=params)
        docs = Document.objects.filter(project=self.main_project).order_by('seq_annotations__updated_at').values()
        for d1, d2 in zip(response.data['results'], docs):
            self.assertEqual(d1['id'], d2['id'])

    def test_can_order_doc_by_annotation_updated_at_descending(self):
        params = {'ordering': '-seq_annotations__updated_at'}
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=params)
        docs = Document.objects.filter(project=self.main_project).order_by('-seq_annotations__updated_at').values()
        for d1, d2 in zip(response.data['results'], docs):
            self.assertEqual(d1['id'], d2['id'])


class TestFilter(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        cls.main_project = mommy.make('server.SequenceLabelingProject', users=[project_member])
        cls.label1 = mommy.make('server.Label', project=cls.main_project)
        cls.label2 = mommy.make('server.Label', project=cls.main_project)
        doc1 = mommy.make('server.Document', project=cls.main_project)
        doc2 = mommy.make('server.Document', project=cls.main_project)
        doc3 = mommy.make('server.Document', project=cls.main_project)
        mommy.make('server.SequenceAnnotation', document=doc1, user=project_member, label=cls.label1)
        mommy.make('server.SequenceAnnotation', document=doc2, user=project_member, label=cls.label2)
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

    def test_can_filter_doc_with_annotation(self):
        params = {'seq_annotations__isnull': False}
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=params)
        docs = Document.objects.filter(project=self.main_project, seq_annotations__isnull=False).values()
        self.assertEqual(response.data['count'], docs.count())
        for d1, d2 in zip(response.data['results'], docs):
            self.assertEqual(d1['id'], d2['id'])

    def test_can_filter_doc_without_anotation(self):
        params = {'seq_annotations__isnull': True}
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=params)
        docs = Document.objects.filter(project=self.main_project, seq_annotations__isnull=True).values()
        self.assertEqual(response.data['count'], docs.count())
        for d1, d2 in zip(response.data['results'], docs):
            self.assertEqual(d1['id'], d2['id'])


class TestUploader(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        cls.classification_project = mommy.make('server.TextClassificationProject',
                                                users=[super_user], project_type=DOCUMENT_CLASSIFICATION)
        cls.labeling_project = mommy.make('server.SequenceLabelingProject',
                                          users=[super_user], project_type=SEQUENCE_LABELING)
        cls.seq2seq_project = mommy.make('server.Seq2seqProject', users=[super_user], project_type=SEQ2SEQ)

    def setUp(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)

    def upload_test_helper(self, project_id, filename, file_format, expected_status, **kwargs):
        url = reverse(viewname='doc_uploader', args=[project_id])

        with open(os.path.join(DATA_DIR, filename)) as f:
            response = self.client.post(url, data={'file': f, 'format': file_format})

        self.assertEqual(response.status_code, expected_status)

    def label_test_helper(self, project_id, expected_labels, expected_label_keys):
        url = reverse(viewname='label_list', args=[project_id])
        expected_keys = {key for label in expected_labels for key in label}

        response = self.client.get(url).json()

        actual_labels = [{key: value for (key, value) in label.items() if key in expected_keys}
                         for label in response]

        self.assertCountEqual(actual_labels, expected_labels)

        for label in response:
            for expected_label_key in expected_label_keys:
                self.assertIsNotNone(label.get(expected_label_key))

    def test_can_upload_conll_format_file(self):
        self.upload_test_helper(project_id=self.labeling_project.id,
                                filename='labeling.conll',
                                file_format='conll',
                                expected_status=status.HTTP_201_CREATED)

    def test_cannot_upload_wrong_conll_format_file(self):
        self.upload_test_helper(project_id=self.labeling_project.id,
                                filename='labeling.invalid.conll',
                                file_format='conll',
                                expected_status=status.HTTP_400_BAD_REQUEST)

    def test_can_upload_classification_csv(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.csv',
                                file_format='csv',
                                expected_status=status.HTTP_201_CREATED)

    def test_can_upload_seq2seq_csv(self):
        self.upload_test_helper(project_id=self.seq2seq_project.id,
                                filename='example.csv',
                                file_format='csv',
                                expected_status=status.HTTP_201_CREATED)

    def test_cannot_upload_csv_file_does_not_match_column_and_row(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.invalid.1.csv',
                                file_format='csv',
                                expected_status=status.HTTP_400_BAD_REQUEST)

    def test_cannot_upload_csv_file_has_too_many_columns(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.invalid.2.csv',
                                file_format='csv',
                                expected_status=status.HTTP_400_BAD_REQUEST)

    def test_can_upload_classification_jsonl(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='classification.jsonl',
                                file_format='json',
                                expected_status=status.HTTP_201_CREATED)

        self.label_test_helper(
            project_id=self.classification_project.id,
            expected_labels=[
                {'text': 'positive', 'suffix_key': 'p', 'prefix_key': None},
                {'text': 'negative', 'suffix_key': 'n', 'prefix_key': None},
                {'text': 'neutral', 'suffix_key': 'n', 'prefix_key': 'ctrl'},
            ],
            expected_label_keys=[
                'background_color',
                'text_color',
            ])

    def test_can_upload_labeling_jsonl(self):
        self.upload_test_helper(project_id=self.labeling_project.id,
                                filename='labeling.jsonl',
                                file_format='json',
                                expected_status=status.HTTP_201_CREATED)

        self.label_test_helper(
            project_id=self.labeling_project.id,
            expected_labels=[
                {'text': 'LOC', 'suffix_key': 'l', 'prefix_key': None},
                {'text': 'ORG', 'suffix_key': 'o', 'prefix_key': None},
                {'text': 'PER', 'suffix_key': 'p', 'prefix_key': None},
            ],
            expected_label_keys=[
                'background_color',
                'text_color',
            ])

    def test_can_upload_seq2seq_jsonl(self):
        self.upload_test_helper(project_id=self.seq2seq_project.id,
                                filename='seq2seq.jsonl',
                                file_format='json',
                                expected_status=status.HTTP_201_CREATED)

    def test_can_upload_plain_text(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.txt',
                                file_format='plain',
                                expected_status=status.HTTP_201_CREATED)

    def test_can_upload_data_without_label(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.jsonl',
                                file_format='json',
                                expected_status=status.HTTP_201_CREATED)


@override_settings(CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER='LOCAL')
@override_settings(CLOUD_BROWSER_APACHE_LIBCLOUD_ACCOUNT=os.path.dirname(DATA_DIR))
@override_settings(CLOUD_BROWSER_APACHE_LIBCLOUD_SECRET_KEY='not-used')
class TestCloudUploader(TestUploader):
    def upload_test_helper(self, project_id, filename, file_format, expected_status, **kwargs):
        query_params = {
            'project_id': project_id,
            'upload_format': file_format,
            'container': kwargs.pop('container', os.path.basename(DATA_DIR)),
            'object': filename,
        }

        query_params.update(kwargs)

        response = self.client.get(reverse('cloud_uploader'), query_params)

        self.assertEqual(response.status_code, expected_status)

    def test_cannot_upload_with_missing_file(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='does-not-exist',
                                file_format='json',
                                expected_status=status.HTTP_400_BAD_REQUEST)

    def test_cannot_upload_with_missing_container(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.jsonl',
                                container='does-not-exist',
                                file_format='json',
                                expected_status=status.HTTP_400_BAD_REQUEST)

    def test_cannot_upload_with_missing_query_parameters(self):
        response = self.client.get(reverse('cloud_uploader'), {'project_id': self.classification_project.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_upload_with_redirect(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.jsonl',
                                next='http://somewhere',
                                file_format='json',
                                expected_status=status.HTTP_302_FOUND)

    def test_can_upload_with_redirect_to_blank(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.jsonl',
                                next='about:blank',
                                file_format='json',
                                expected_status=status.HTTP_201_CREATED)


class TestFeatures(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_name = 'user_name'
        cls.user_pass = 'user_pass'

        cls.user = User.objects.create_user(username=cls.user_name, password=cls.user_pass, email='fizz@buzz.com')

    def setUp(self):
        self.client.login(username=self.user_name, password=self.user_pass)

    @override_settings(CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER=None)
    def test_no_cloud_upload(self):
        response = self.client.get(reverse('features'))

        self.assertFalse(response.json().get('cloud_upload'))


@override_settings(IMPORT_BATCH_SIZE=2)
class TestParser(APITestCase):

    def parser_helper(self, filename, parser, include_label=True):
        with open(os.path.join(DATA_DIR, filename), mode='rb') as f:
            result = list(parser.parse(f))
            for data in result:
                for r in data:
                    self.assertIn('text', r)
                    if include_label:
                        self.assertIn('labels', r)
        return result

    def test_give_valid_data_to_conll_parser(self):
        self.parser_helper(filename='labeling.conll', parser=CoNLLParser())

    def test_give_valid_data_to_conll_parser_with_trailing_newlines(self):
        result = self.parser_helper(filename='labeling.trailing.conll', parser=CoNLLParser())
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 1)

    def test_plain_parser(self):
        self.parser_helper(filename='example.txt', parser=PlainTextParser(), include_label=False)

    def test_give_invalid_data_to_conll_parser(self):
        with self.assertRaises(FileParseException):
            self.parser_helper(filename='labeling.invalid.conll',
                               parser=CoNLLParser())

    def test_give_classification_data_to_csv_parser(self):
        self.parser_helper(filename='example.csv', parser=CSVParser())

    def test_give_seq2seq_data_to_csv_parser(self):
        self.parser_helper(filename='example.csv', parser=CSVParser())

    def test_give_classification_data_to_json_parser(self):
        self.parser_helper(filename='classification.jsonl', parser=JSONParser())

    def test_give_labeling_data_to_json_parser(self):
        self.parser_helper(filename='labeling.jsonl', parser=JSONParser())

    def test_give_seq2seq_data_to_json_parser(self):
        self.parser_helper(filename='seq2seq.jsonl', parser=JSONParser())

    def test_give_data_without_label_to_json_parser(self):
        self.parser_helper(filename='example.jsonl', parser=JSONParser(), include_label=False)


class TestDownloader(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        cls.classification_project = mommy.make('server.TextClassificationProject',
                                                users=[super_user], project_type=DOCUMENT_CLASSIFICATION)
        cls.labeling_project = mommy.make('server.SequenceLabelingProject',
                                          users=[super_user], project_type=SEQUENCE_LABELING)
        cls.seq2seq_project = mommy.make('server.Seq2seqProject', users=[super_user], project_type=SEQ2SEQ)
        cls.classification_url = reverse(viewname='doc_downloader', args=[cls.classification_project.id])
        cls.labeling_url = reverse(viewname='doc_downloader', args=[cls.labeling_project.id])
        cls.seq2seq_url = reverse(viewname='doc_downloader', args=[cls.seq2seq_project.id])

    def setUp(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)

    def download_test_helper(self, url, format, expected_status):
        response = self.client.get(url, data={'q': format})
        self.assertEqual(response.status_code, expected_status)

    def test_cannot_download_conll_format_file(self):
        self.download_test_helper(url=self.labeling_url,
                                  format='conll',
                                  expected_status=status.HTTP_400_BAD_REQUEST)

    def test_can_download_classification_csv(self):
        self.download_test_helper(url=self.classification_url,
                                  format='csv',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_labeling_csv(self):
        self.download_test_helper(url=self.labeling_url,
                                  format='csv',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_seq2seq_csv(self):
        self.download_test_helper(url=self.seq2seq_url,
                                  format='csv',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_classification_jsonl(self):
        self.download_test_helper(url=self.classification_url,
                                  format='json',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_labeling_jsonl(self):
        self.download_test_helper(url=self.labeling_url,
                                  format='json',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_seq2seq_jsonl(self):
        self.download_test_helper(url=self.seq2seq_url,
                                  format='json',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_labelling_json1(self):
        self.download_test_helper(url=self.labeling_url,
                                  format='json1',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_plain_text(self):
        self.download_test_helper(url=self.classification_url,
                                  format='plain',
                                  expected_status=status.HTTP_400_BAD_REQUEST)


class TestStatisticsAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')

        main_project = mommy.make('server.TextClassificationProject', users=[super_user])
        doc1 = mommy.make('server.Document', project=main_project)
        doc2 = mommy.make('server.Document', project=main_project)
        mommy.make('DocumentAnnotation', document=doc1, user=super_user)
        cls.url = reverse(viewname='statistics', args=[main_project.id])
        cls.doc = Document.objects.filter(project=main_project)

    def test_returns_exact_progress(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.get(self.url, format='json')
        total = self.doc.count()
        remaining = self.doc.filter(doc_annotations__isnull=True).count()
        self.assertEqual(response.data['total'], total)
        self.assertEqual(response.data['remaining'], remaining)

    def test_returns_user_count(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.get(self.url, format='json')
        self.assertIn('label', response.data)
        self.assertIsInstance(response.data['label'], dict)

    def test_returns_label_count(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.get(self.url, format='json')
        self.assertIn('user', response.data)
        self.assertIsInstance(response.data['user'], dict)
