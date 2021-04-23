from django.conf import settings
from django.contrib.auth.models import User
from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import SequenceAnnotation
from .utils import (TestUtilsMixin, assign_user_to_role, create_default_roles,
                    remove_all_role_mappings)


class TestAnnotationListAPI(APITestCase, TestUtilsMixin):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.another_project_member_name = 'another_project_member_name'
        cls.another_project_member_pass = 'another_project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        create_default_roles()
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        another_project_member = User.objects.create_user(username=cls.another_project_member_name,
                                                          password=cls.another_project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)

        main_project = mommy.make('SequenceLabelingProject', users=[project_member, another_project_member])
        main_project_label = mommy.make('Label', project=main_project)
        main_project_doc = mommy.make('Document', project=main_project)
        mommy.make('SequenceAnnotation', document=main_project_doc, user=project_member)
        mommy.make('SequenceAnnotation', document=main_project_doc, user=another_project_member)

        sub_project = mommy.make('SequenceLabelingProject', users=[non_project_member])
        sub_project_doc = mommy.make('Document', project=sub_project)
        mommy.make('SequenceAnnotation', document=sub_project_doc)

        cls.classification_project = mommy.make('TextClassificationProject',
                                                users=[project_member, another_project_member])
        cls.classification_project_label_1 = mommy.make('Label', project=cls.classification_project)
        cls.classification_project_label_2 = mommy.make('Label', project=cls.classification_project)
        cls.classification_project_document = mommy.make('Document', project=cls.classification_project)
        cls.classification_project_url = reverse(
            viewname='annotation_list', args=[cls.classification_project.id, cls.classification_project_document.id])
        assign_user_to_role(project_member=project_member, project=cls.classification_project,
                            role_name=settings.ROLE_ANNOTATOR)
        assign_user_to_role(project_member=another_project_member, project=cls.classification_project,
                            role_name=settings.ROLE_ANNOTATOR)

        cls.url = reverse(viewname='annotation_list', args=[main_project.id, main_project_doc.id])
        cls.post_data = {'start_offset': 0, 'end_offset': 1, 'label': main_project_label.id}
        cls.num_entity_of_project_member = SequenceAnnotation.objects.filter(document=main_project_doc,
                                                                             user=project_member).count()
        cls.num_entity_of_another_project_member = SequenceAnnotation.objects.filter(
            document=main_project_doc,
            user=another_project_member).count()
        cls.main_project = main_project
        assign_user_to_role(project_member=project_member, project=main_project,
                            role_name=settings.ROLE_ANNOTATOR)

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

    def test_returns_annotations_of_another_project_member_if_collaborative_project(self):
        self._patch_project(self.main_project, 'collaborative_annotation', True)

        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data),
                         self.num_entity_of_project_member + self.num_entity_of_another_project_member)

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

    def test_allow_replace_annotation_for_single_class_project(self):
        self._patch_project(self.classification_project, 'single_class_classification', True)

        self.client.login(username=self.project_member_name, password=self.project_member_pass)
        response = self.client.post(self.classification_project_url, format='json',
                                    data={'label': self.classification_project_label_1.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.classification_project_url, format='json',
                                    data={'label': self.classification_project_label_2.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_allow_replace_annotation_for_single_class_shared_project(self):
        self._patch_project(self.classification_project, 'single_class_classification', True)
        self._patch_project(self.classification_project, 'collaborative_annotation', True)

        self.client.login(username=self.project_member_name, password=self.project_member_pass)
        response = self.client.post(self.classification_project_url, format='json',
                                    data={'label': self.classification_project_label_1.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.login(username=self.another_project_member_name, password=self.another_project_member_pass)
        response = self.client.post(self.classification_project_url, format='json',
                                    data={'label': self.classification_project_label_2.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def _patch_project(self, project, attribute, value):
        old_value = getattr(project, attribute, None)
        setattr(project, attribute, value)
        project.save()

        def cleanup_project():
            setattr(project, attribute, old_value)
            project.save()

        self.addCleanup(cleanup_project)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


class TestAnnotationDetailAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.another_project_member_name = 'another_project_member_name'
        cls.another_project_member_pass = 'another_project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        create_default_roles()
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        another_project_member = User.objects.create_user(username=cls.another_project_member_name,
                                                          password=cls.another_project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)

        main_project = mommy.make('SequenceLabelingProject',
                                  users=[super_user, project_member, another_project_member])
        main_project_doc = mommy.make('Document', project=main_project)
        main_project_entity = mommy.make('SequenceAnnotation',
                                         document=main_project_doc, user=project_member)
        another_entity = mommy.make('SequenceAnnotation',
                                    document=main_project_doc, user=another_project_member)

        shared_project = mommy.make('SequenceLabelingProject',
                                    collaborative_annotation=True,
                                    users=[project_member, another_project_member])
        shared_project_doc = mommy.make('Document', project=shared_project)
        shared_entity = mommy.make('SequenceAnnotation', document=shared_project_doc, user=another_project_member)

        cls.url = reverse(viewname='annotation_detail', args=[main_project.id,
                                                              main_project_doc.id,
                                                              main_project_entity.id])
        cls.another_url = reverse(viewname='annotation_detail', args=[main_project.id,
                                                                      main_project_doc.id,
                                                                      another_entity.id])
        cls.shared_url = reverse(viewname='annotation_detail', args=[shared_project.id,
                                                                     shared_project_doc.id,
                                                                     shared_entity.id])
        cls.post_data = {'start_offset': 0, 'end_offset': 10}
        assign_user_to_role(project_member=project_member, project=main_project, role_name=settings.ROLE_ANNOTATOR)
        assign_user_to_role(project_member=project_member, project=shared_project, role_name=settings.ROLE_ANNOTATOR)

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

    def test_allows_superuser_to_delete_annotation_of_another_member(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.delete(self.another_url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

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

    def test_allow_member_to_update_others_annotation_in_shared_project(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.shared_url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_allow_member_to_delete_others_annotation_in_shared_project(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.delete(self.shared_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()
