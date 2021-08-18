from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse

from .utils import (CRUDMixin, assign_user_to_role, make_doc,
                    make_example_state, make_user, prepare_project)


class TestExampleStateList(CRUDMixin):

    @classmethod
    def setUpTestData(cls):
        cls.non_member = make_user()
        cls.project = prepare_project()
        cls.example = make_doc(cls.project.item)
        for user in cls.project.users:
            make_example_state(cls.example, user)
        cls.url = reverse(viewname='example_state_list', args=[cls.project.item.id, cls.example.id])

    def test_returns_example_state_to_project_member(self):
        for member in self.project.users:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data['count'], 1)

    def test_does_not_return_example_state_to_non_project_member(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_does_not_return_example_state_to_unauthenticated_user(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)


class TestExampleStateConfirm(CRUDMixin):

    def setUp(self):
        self.project = prepare_project()
        self.example = make_doc(self.project.item)
        self.url = reverse(viewname='example_state_list', args=[self.project.item.id, self.example.id])

    def test_allows_member_to_confirm_example(self):
        for member in self.project.users:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data['count'], 0)
            self.assert_create(member, status.HTTP_201_CREATED)  # confirm
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data['count'], 1)
            self.assert_create(member, status.HTTP_201_CREATED)  # toggle confirm
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data['count'], 0)


class TestExampleStateConfirmCollaborative(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(collaborative_annotation=True)
        self.example = make_doc(self.project.item)
        self.url = reverse(viewname='example_state_list', args=[self.project.item.id, self.example.id])

    def test_cannot_share_example_state_in_other_role(self):
        admin = self.project.users[0]
        approver = self.project.users[1]
        response = self.assert_fetch(admin, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        response = self.assert_fetch(approver, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        self.assert_create(admin, status.HTTP_201_CREATED)  # confirm by admin
        response = self.assert_fetch(admin, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        response = self.assert_fetch(approver, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        self.assert_create(approver, status.HTTP_201_CREATED)  # confirm by approver
        response = self.assert_fetch(admin, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        response = self.assert_fetch(approver, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_can_share_example_state_in_same_role(self):
        annotator1 = make_user()
        assign_user_to_role(annotator1, self.project.item, settings.ROLE_ANNOTATOR)
        annotator2 = make_user()
        assign_user_to_role(annotator2, self.project.item, settings.ROLE_ANNOTATOR)

        response = self.assert_fetch(annotator1, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        response = self.assert_fetch(annotator2, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        self.assert_create(annotator1, status.HTTP_201_CREATED)  # confirm by annotator1
        response = self.assert_fetch(annotator1, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        response = self.assert_fetch(annotator2, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        self.assert_create(annotator2, status.HTTP_201_CREATED)  # toggle confirm by annotator2
        response = self.assert_fetch(annotator1, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        response = self.assert_fetch(annotator2, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
