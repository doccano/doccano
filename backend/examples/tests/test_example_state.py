from rest_framework import status
from rest_framework.reverse import reverse

from .utils import make_doc, make_example_state
from api.tests.utils import CRUDMixin
from projects.tests.utils import prepare_project
from users.tests.utils import make_user


class TestExampleStateList(CRUDMixin):
    @classmethod
    def setUpTestData(cls):
        cls.non_member = make_user()
        cls.project = prepare_project()
        cls.example = make_doc(cls.project.item)
        for member in cls.project.members:
            make_example_state(cls.example, member)
        cls.url = reverse(viewname="example_state_list", args=[cls.project.item.id, cls.example.id])

    def test_returns_example_state_to_project_member(self):
        for member in self.project.members:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)

    def test_does_not_return_example_state_to_non_project_member(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_does_not_return_example_state_to_unauthenticated_user(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)


class TestExampleStateConfirm(CRUDMixin):
    def setUp(self):
        self.project = prepare_project()
        self.example = make_doc(self.project.item)
        self.url = reverse(viewname="example_state_list", args=[self.project.item.id, self.example.id])

    def test_allows_member_to_confirm_example(self):
        for member in self.project.members:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 0)
            self.assert_create(member, status.HTTP_201_CREATED)  # confirm
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)
            self.assert_create(member, status.HTTP_201_CREATED)  # toggle confirm
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 0)


class TestExampleStateConfirmCollaborative(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(collaborative_annotation=True)
        self.example = make_doc(self.project.item)
        self.url = reverse(viewname="example_state_list", args=[self.project.item.id, self.example.id])

    def test_initial_state(self):
        for member in self.project.members:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 0)

    def test_can_approve_state(self):
        admin = self.project.admin
        self.assert_create(admin, status.HTTP_201_CREATED)
        for member in self.project.members:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)
