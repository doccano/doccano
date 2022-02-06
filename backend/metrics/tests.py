from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.utils import CRUDMixin
from examples.tests.utils import make_doc
from label_types.tests.utils import make_label
from projects.models import DOCUMENT_CLASSIFICATION
from projects.tests.utils import prepare_project


class TestMemberProgress(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(DOCUMENT_CLASSIFICATION)
        self.example = make_doc(self.project.item)
        self.url = reverse(viewname="member_progress", args=[self.project.item.id])

    def test_fetch_initial_progress(self):
        response = self.assert_fetch(self.project.admin, status.HTTP_200_OK)
        expected_progress = [{"user": member.username, "done": 0} for member in self.project.members]
        self.assertEqual(response.data, {"total": 1, "progress": expected_progress})

    def test_fetch_progress(self):
        mommy.make("ExampleState", example=self.example, confirmed_by=self.project.admin)
        response = self.assert_fetch(self.project.admin, status.HTTP_200_OK)
        expected_progress = [{"user": member.username, "done": 0} for member in self.project.members]
        expected_progress[0]["done"] = 1
        self.assertEqual(response.data, {"total": 1, "progress": expected_progress})


class TestCategoryDistribution(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(DOCUMENT_CLASSIFICATION)
        self.example = make_doc(self.project.item)
        self.label = make_label(self.project.item, text="label")
        mommy.make("Category", example=self.example, label=self.label, user=self.project.admin)
        self.url = reverse(viewname="category_distribution", args=[self.project.item.id])

    def test_fetch_distribution(self):
        response = self.assert_fetch(self.project.admin, status.HTTP_200_OK)
        expected = {member.username: {self.label.text: 0} for member in self.project.members}
        expected[self.project.admin.username][self.label.text] = 1
        self.assertEqual(response.data, expected)
