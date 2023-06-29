from unittest.mock import MagicMock

from django.test import TestCase
from model_mommy import mommy

from .utils import make_doc, make_example_state
from examples.filters import ExampleFilter
from examples.models import Example
from projects.models import ProjectType
from projects.tests.utils import prepare_project


class TestFilterMixin(TestCase):
    def prepare(self, project):
        self.example = make_doc(project.item)
        self.request = MagicMock()
        self.queryset = Example.objects.all()
        make_example_state(self.example, project.admin)
        self.request.user = project.admin

    def assert_filter(self, data, expected):
        f = ExampleFilter(data=data, queryset=self.queryset, request=self.request)
        self.assertEqual(f.qs.count(), expected)


class TestExampleFilter(TestFilterMixin):
    def setUp(self):
        self.project = prepare_project(task="DocumentClassification")
        self.prepare(project=self.project)

    def test_returns_example_if_confirmed_is_true(self):
        self.assert_filter(data={"confirmed": "True"}, expected=1)

    def test_does_not_return_example_if_confirmed_is_false(self):
        self.assert_filter(data={"confirmed": "False"}, expected=0)

    def test_returns_example_if_confirmed_is_empty(self):
        self.assert_filter(data={"confirmed": ""}, expected=1)

    def test_does_not_return_example_if_user_is_different(self):
        self.request.user = self.project.approver
        self.assert_filter(data={"confirmed": "True"}, expected=0)

    def test_returns_example_if_user_is_different(self):
        self.request.user = self.project.approver
        self.assert_filter(data={"confirmed": "False"}, expected=1)

    def test_returns_example_if_user_is_different_and_confirmed_is_empty(self):
        self.request.user = self.project.approver
        self.assert_filter(data={"confirmed": ""}, expected=1)


class TestLabelFilter(TestFilterMixin):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.DOCUMENT_CLASSIFICATION)
        self.prepare(project=self.project)
        self.label_type = mommy.make("CategoryType", project=self.project.item, text="positive")
        mommy.make("Category", example=self.example, label=self.label_type)

    def test_returns_example_with_positive_label(self):
        self.assert_filter(data={"label": self.label_type.text}, expected=1)


class TestExampleFilterOnCollaborative(TestFilterMixin):
    def setUp(self):
        self.project = prepare_project(task="DocumentClassification", collaborative_annotation=True)
        self.prepare(project=self.project)

    def test_returns_example_if_confirmed_is_true(self):
        for member in self.project.members:
            self.request.user = member
            self.assert_filter(data={"confirmed": "True"}, expected=1)

    def test_does_not_return_example_if_confirmed_is_false(self):
        for member in self.project.members:
            self.request.user = member
            self.assert_filter(data={"confirmed": "False"}, expected=0)

    def test_returns_example_if_confirmed_is_empty(self):
        for member in self.project.members:
            self.request.user = member
            self.assert_filter(data={"confirmed": ""}, expected=1)
