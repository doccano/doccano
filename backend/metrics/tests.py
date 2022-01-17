from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.api.utils import CRUDMixin, prepare_project, make_doc, make_label
from api.models import DOCUMENT_CLASSIFICATION


class TestMemberProgress(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(DOCUMENT_CLASSIFICATION)
        self.example = make_doc(self.project.item)
        self.url = reverse(viewname='member_progress', args=[self.project.item.id])

    def test_fetch_initial_progress(self):
        response = self.assert_fetch(self.project.users[0], status.HTTP_200_OK)
        expected_progress = [{'user': user.username, 'done': 0} for user in self.project.users]
        self.assertEqual(response.data, {'total': 1, 'progress': expected_progress})

    def test_fetch_progress(self):
        mommy.make('ExampleState', example=self.example, confirmed_by=self.project.users[0])
        response = self.assert_fetch(self.project.users[0], status.HTTP_200_OK)
        expected_progress = [{'user': user.username, 'done': 0} for user in self.project.users]
        expected_progress[0]['done'] = 1
        self.assertEqual(response.data, {'total': 1, 'progress': expected_progress})


class TestCategoryDistribution(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(DOCUMENT_CLASSIFICATION)
        self.example = make_doc(self.project.item)
        self.label = make_label(self.project.item, text='label')
        mommy.make('Category', example=self.example, label=self.label, user=self.project.users[0])
        self.url = reverse(viewname='category_distribution', args=[self.project.item.id])

    def test_fetch_distribution(self):
        response = self.assert_fetch(self.project.users[0], status.HTTP_200_OK)
        expected = {
            user.username: {self.label.text: 0} for user in self.project.users
        }
        expected[self.project.users[0].username][self.label.text] = 1
        self.assertEqual(response.data, expected)
