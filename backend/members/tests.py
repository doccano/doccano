from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse

from roles.models import Role
from members.models import Member
from api.tests.api.utils import (CRUDMixin, prepare_project, make_user)


class TestMemberListAPI(CRUDMixin):

    def setUp(self):
        self.project = prepare_project()
        self.non_member = make_user()
        admin_role = Role.objects.get(name=settings.ROLE_PROJECT_ADMIN)
        self.data = {'user': self.non_member.id, 'role': admin_role.id, 'project': self.project.item.id}
        self.url = reverse(viewname='member_list', args=[self.project.item.id])

    def test_allows_project_admin_to_get_mappings(self):
        self.assert_fetch(self.project.users[0], status.HTTP_200_OK)

    def test_denies_non_project_admin_to_get_mappings(self):
        for member in self.project.users[1:]:
            self.assert_fetch(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_get_mappings(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_get_mappings(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_project_admin_to_create_mapping(self):
        self.assert_create(self.project.users[0], status.HTTP_201_CREATED)

    def test_denies_non_project_admin_to_create_mapping(self):
        for member in self.project.users[1:]:
            self.assert_create(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_create_mapping(self):
        self.assert_create(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_create_mapping(self):
        self.assert_create(expected=status.HTTP_403_FORBIDDEN)

    def assert_bulk_delete(self, user=None, expected=status.HTTP_403_FORBIDDEN):
        if user:
            self.client.force_login(user)
        ids = [item.id for item in self.project.item.role_mappings.all()]
        response = self.client.delete(self.url, data={'ids': ids}, format='json')
        self.assertEqual(response.status_code, expected)

    def test_allows_project_admin_to_bulk_delete(self):
        self.assert_bulk_delete(self.project.users[0], status.HTTP_204_NO_CONTENT)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 1)

    def test_denies_non_project_admin_to_bulk_delete(self):
        for member in self.project.users[1:]:
            self.assert_bulk_delete(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_bulk_delete(self):
        self.assert_bulk_delete(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_bulk_delete(self):
        self.assert_bulk_delete(expected=status.HTTP_403_FORBIDDEN)


class TestMemberRoleDetailAPI(CRUDMixin):

    def setUp(self):
        self.project = prepare_project()
        self.non_member = make_user()
        admin_role = Role.objects.get(name=settings.ROLE_PROJECT_ADMIN)
        mapping = Member.objects.get(user=self.project.users[1])
        self.url = reverse(viewname='member_detail', args=[self.project.item.id, mapping.id])
        self.data = {'role': admin_role.id}

    def test_allows_project_admin_to_get_mapping(self):
        self.assert_fetch(self.project.users[0], status.HTTP_200_OK)

    def test_denies_non_project_admin_to_get_mapping(self):
        for member in self.project.users[1:]:
            self.assert_fetch(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_get_mapping(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_get_mapping(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_project_admin_to_update_mapping(self):
        self.assert_update(self.project.users[0], status.HTTP_200_OK)

    def test_denies_non_project_admin_to_update_mapping(self):
        for member in self.project.users[1:]:
            self.assert_update(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_update_mapping(self):
        self.assert_update(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_update_mapping(self):
        self.assert_update(expected=status.HTTP_403_FORBIDDEN)


class TestMemberFilter(CRUDMixin):

    def setUp(self):
        self.project = prepare_project()
        self.url = reverse(viewname='member_list', args=[self.project.item.id])
        self.url += f'?user={self.project.users[0].id}'

    def test_filter_role_by_user_id(self):
        response = self.assert_fetch(self.project.users[0], status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TestMemberManager(CRUDMixin):

    def setUp(self):
        pass

    def test_has_role(self):
        project = prepare_project()
        admin = project.users[0]
        expected = [
            (settings.ROLE_PROJECT_ADMIN, True),
            (settings.ROLE_ANNOTATION_APPROVER, False),
            (settings.ROLE_ANNOTATOR, False)
        ]
        for role, expect in expected:
            self.assertEqual(Member.objects.has_role(project.item, admin, role), expect)
