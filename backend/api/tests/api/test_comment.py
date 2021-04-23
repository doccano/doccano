from django.conf import settings
from django.contrib.auth.models import User
from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .utils import (assign_user_to_role, create_default_roles,
                    remove_all_role_mappings)


class TestCommentListAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.another_project_member_name = 'another_project_member_name'
        cls.another_project_member_pass = 'another_project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        create_default_roles()
        cls.project_member = User.objects.create_user(username=cls.project_member_name,
                                                    password=cls.project_member_pass)
        another_project_member = User.objects.create_user(username=cls.another_project_member_name,
                                                        password=cls.another_project_member_pass)
        User.objects.create_user(username=cls.non_project_member_name, password=cls.non_project_member_pass)

        main_project = mommy.make('SequenceLabelingProject', users=[cls.project_member, another_project_member])
        main_project_doc = mommy.make('Document', project=main_project)
        cls.comment = mommy.make('Comment', document=main_project_doc, text='comment 1', user=cls.project_member)
        mommy.make('Comment', document=main_project_doc, text='comment 2', user=cls.project_member)
        mommy.make('Comment', document=main_project_doc, text='comment 3', user=another_project_member)

        cls.url = reverse(viewname='comment_list_doc', args=[main_project.id, main_project_doc.id])
        cls.url_project = reverse(viewname='comment_list_project', args=[main_project.id])

        assign_user_to_role(project_member=cls.project_member, project=main_project,
                            role_name=settings.ROLE_ANNOTATOR)
        assign_user_to_role(project_member=another_project_member, project=main_project,
                            role_name=settings.ROLE_ANNOTATOR)

    def test_returns_comments_to_project_member(self):
        self.client.login(username=self.project_member_name,
                        password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        self.client.login(username=self.another_project_member_name,
                        password=self.another_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_does_not_return_comments_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                        password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_does_not_allow_deletion_by_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                        password=self.non_project_member_pass)
        response = self.client.delete('{}/{}'.format(self.url, self.comment.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_does_not_allow_deletion_of_non_owned_comment(self):
        self.client.login(username=self.another_project_member_name,
                        password=self.another_project_member_pass)
        response = self.client.delete('{}/{}'.format(self.url, self.comment.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_update_delete_comment(self):
        self.client.login(username=self.project_member_name,
                        password=self.project_member_pass)
        response = self.client.post(self.url, format='json', data={'text': 'comment'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.project_member.id)
        self.assertEqual(response.data['text'], 'comment')
        url = '{}/{}'.format(self.url, response.data['id'])

        # check if all comments are fetched
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        # update comment
        response = self.client.patch(url, format='json', data={'text': 'new comment'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'new comment')

        # delete comment
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_returns_project_comments_to_project_member(self):
        self.client.login(username=self.project_member_name,
                        password=self.project_member_pass)
        response = self.client.get(self.url_project, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        self.client.login(username=self.another_project_member_name,
                        password=self.another_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_does_not_return_project_comments_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                        password=self.non_project_member_pass)
        response = self.client.get(self.url_project, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()
