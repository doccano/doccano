from rest_framework import status
from rest_framework.reverse import reverse

from .utils import make_assignment, make_doc
from api.tests.utils import CRUDMixin
from examples.models import Assignment
from projects.models import Member
from projects.tests.utils import prepare_project
from users.tests.utils import make_user


class TestAssignmentList(CRUDMixin):
    def setUp(self):
        self.project = prepare_project()
        self.non_member = make_user()
        self.example = make_doc(self.project.item)
        make_assignment(self.project.item, self.example, self.project.admin)
        self.data = {"example": self.example.id, "assignee": self.project.staffs[0].id}
        self.url = reverse(viewname="assignment_list", args=[self.project.item.id])

    def test_allow_project_member_to_list_assignments(self):
        for member in self.project.members:
            self.assert_fetch(member, status.HTTP_200_OK)

    def test_denies_non_project_member_to_list_assignments(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_list_assignments(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_project_admin_to_assign(self):
        response = self.assert_create(self.project.admin, status.HTTP_201_CREATED)
        self.assertEqual(response.data["example"], self.data["example"])
        self.assertEqual(response.data["assignee"], self.data["assignee"])

    def test_denies_non_admin_to_assign(self):
        for member in self.project.staffs:
            self.assert_create(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_assign(self):
        self.assert_create(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_assign(self):
        self.assert_create(expected=status.HTTP_403_FORBIDDEN)


class TestAssignmentDetail(CRUDMixin):
    def setUp(self):
        self.project = prepare_project()
        self.non_member = make_user()
        example = make_doc(self.project.item)
        assignment = make_assignment(self.project.item, example, self.project.admin)
        self.data = {"assignee": self.project.staffs[0].id}
        self.url = reverse(viewname="assignment_detail", args=[self.project.item.id, assignment.id])

    def test_allows_project_member_to_get_assignment(self):
        for member in self.project.members:
            self.assert_fetch(member, status.HTTP_200_OK)

    def test_denies_non_project_member_to_get_assignment(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_get_assignment(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_project_admin_to_reassign(self):
        response = self.assert_update(self.project.admin, status.HTTP_200_OK)
        self.assertEqual(response.data["assignee"], self.data["assignee"])

    def test_denies_non_admin_to_reassign(self):
        for member in self.project.staffs:
            self.assert_update(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_reassign(self):
        self.assert_update(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_reassign(self):
        self.assert_update(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_project_admin_to_unassign(self):
        self.assert_delete(self.project.admin, status.HTTP_204_NO_CONTENT)

    def test_denies_non_admin_to_unassign(self):
        for member in self.project.staffs:
            self.assert_delete(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_unassign(self):
        self.assert_delete(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_unassign(self):
        self.assert_delete(expected=status.HTTP_403_FORBIDDEN)


class TestAssignmentBulk(CRUDMixin):
    def setUp(self):
        self.project = prepare_project()
        self.non_member = make_user()
        self.example = make_doc(self.project.item)
        members = Member.objects.filter(project=self.project.item)
        workloads = [{"member_id": member.id, "weight": 100} for member in members]
        self.data = {"strategy_name": "sampling_without_replacement", "workloads": workloads}
        self.url = reverse(viewname="bulk_assignment", args=[self.project.item.id])

    def test_denies_non_admin_to_bulk_assign(self):
        for member in self.project.staffs:
            self.assert_create(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_bulk_assign(self):
        self.assert_create(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_bulk_assign(self):
        self.assert_create(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_project_admin_to_bulk_assign(self):
        self.assert_create(self.project.admin, status.HTTP_201_CREATED)
        expected = self.project.item.examples.count() * len(self.project.members)
        self.assertEqual(Assignment.objects.count(), expected)
