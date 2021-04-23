from django.conf import settings
from django.contrib.auth.models import User
from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import Role
from .utils import assign_user_to_role, create_default_roles


class TestRoleAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_name = 'user_name'
        cls.user_pass = 'user_pass'
        cls.project_admin_name = 'project_admin_name'
        cls.project_admin_pass = 'project_admin_pass'
        create_default_roles()
        cls.user = User.objects.create_user(username=cls.user_name,
                                            password=cls.user_pass)
        User.objects.create_superuser(username=cls.project_admin_name,
                                      password=cls.project_admin_pass,
                                      email='fizz@buzz.com')
        cls.url = reverse(viewname='roles')

    def test_cannot_create_multiple_roles_with_same_name(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        roles = [
            {'name': 'examplerole', 'description': 'example'},
            {'name': 'examplerole', 'description': 'example'}
        ]
        self.client.post(self.url, format='json', data=roles[0])
        second_response = self.client.post(self.url, format='json', data=roles[1])
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nonadmin_cannot_create_role(self):
        self.client.login(username=self.user_name,
                          password=self.user_pass)
        data = {'name': 'testrole', 'description': 'example'}
        response = self.client.post(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_role(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        data = {'name': 'testrole', 'description': 'example'}
        response = self.client.post(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_get_roles(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRoleMappingListAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.second_project_member_name = 'second_project_member_name'
        cls.second_project_member_pass = 'second_project_member_pass'
        cls.project_admin_name = 'project_admin_name'
        cls.project_admin_pass = 'project_admin_pass'
        create_default_roles()
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                      password=cls.project_member_pass)
        cls.second_project_member = User.objects.create_user(username=cls.second_project_member_name,
                                                      password=cls.second_project_member_pass)
        project_admin = User.objects.create_user(username=cls.project_admin_name,
                                                   password=cls.project_admin_pass)
        cls.main_project = mommy.make('Project', users=[project_member, project_admin, cls.second_project_member])
        cls.other_project = mommy.make('Project', users=[cls.second_project_member, project_admin])
        cls.admin_role = Role.objects.get(name=settings.ROLE_PROJECT_ADMIN)
        cls.role = mommy.make('Role', name='otherrole')
        assign_user_to_role(project_admin, cls.main_project, cls.admin_role)
        cls.data = {'user': project_member.id, 'role': cls.admin_role.id, 'project': cls.main_project.id}
        cls.other_url = reverse(viewname='rolemapping_list', args=[cls.other_project.id])
        cls.url = reverse(viewname='rolemapping_list', args=[cls.main_project.id])

    def test_returns_mappings_to_project_admin(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Todo: refactoring testing.
    # def test_allows_superuser_to_create_mapping(self):
    #     self.client.login(username=self.project_admin_name,
    #                       password=self.project_admin_pass)
    #     response = self.client.post(self.url, format='json', data=self.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    # def test_do_not_allow_nonadmin_to_create_mapping(self):
    #     self.client.login(username=self.project_member_name,
    #                       password=self.project_member_pass)
    #     response = self.client.post(self.url, format='json', data=self.data)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    # def test_do_not_return_mappings_to_nonadmin(self):
    #     self.client.login(username=self.project_member_name,
    #                       password=self.project_member_pass)
    #     response = self.client.get(self.url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRoleMappingDetailAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_admin_name = 'project_admin_name'
        cls.project_admin_pass = 'project_admin_pass'
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        create_default_roles()
        project_admin = User.objects.create_user(username=cls.project_admin_name,
                                                   password=cls.project_admin_pass)
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                      password=cls.project_member_pass)
        User.objects.create_user(username=cls.non_project_member_name, password=cls.non_project_member_pass)
        project = mommy.make('Project', users=[project_admin, project_member])
        admin_role = Role.objects.get(name=settings.ROLE_PROJECT_ADMIN)
        annotator_role = Role.objects.get(name=settings.ROLE_ANNOTATOR)
        cls.rolemapping = assign_user_to_role(project_admin, project, admin_role)
        assign_user_to_role(project_member, project, annotator_role)
        cls.url = reverse(viewname='rolemapping_detail', args=[project.id, cls.rolemapping.id])
        cls.data = {'role': admin_role.id}

    def test_returns_rolemapping_to_project_member(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['id'], self.rolemapping.id)

    def test_do_not_return_mapping_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_admin_to_update_mapping(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        response = self.client.patch(self.url, format='json', data=self.data)
        self.assertEqual(response.data['role'], self.data['role'])

    def test_disallows_project_member_to_update_mapping(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_admin_to_delete_mapping(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_disallows_project_member_to_delete_mapping(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
