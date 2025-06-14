import pathlib
from unittest.mock import patch

from auto_labeling_pipeline.mappings import AmazonComprehendSentimentTemplate
from auto_labeling_pipeline.models import RequestModelFactory
from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.utils import CRUDMixin
from auto_labeling.pipeline.labels import Categories, Spans, Texts
from examples.tests.utils import make_doc
from labels.models import Category, Span, TextLabel
from projects.models import ProjectType
from projects.tests.utils import prepare_project

data_dir = pathlib.Path(__file__).parent / "data"


class TestTemplateList(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.DOCUMENT_CLASSIFICATION)
        self.url = reverse(viewname="auto_labeling_templates", args=[self.project.item.id])

    def test_allow_admin_to_fetch_template_list(self):
        self.url += "?task_name=DocumentClassification"
        response = self.assert_fetch(self.project.admin, status.HTTP_200_OK)
        self.assertIn("Custom REST Request", response.data)
        self.assertGreaterEqual(len(response.data), 1)

    def test_deny_project_staff_to_fetch_template_list(self):
        self.url += "?task_name=DocumentClassification"
        for user in self.project.staffs:
            self.assert_fetch(user, status.HTTP_403_FORBIDDEN)

    def test_return_only_default_template_with_empty_task_name(self):
        response = self.assert_fetch(self.project.admin, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("Custom REST Request", response.data)

    def test_return_only_default_template_with_wrong_task_name(self):
        self.url += "?task_name=foobar"
        response = self.assert_fetch(self.project.admin, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("Custom REST Request", response.data)


class TestConfigParameter(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.DOCUMENT_CLASSIFICATION)
        self.data = {
            "model_name": "GCP Entity Analysis",
            "model_attrs": {"key": "hoge", "type": "PLAIN_TEXT", "language": "en"},
            "text": "example",
        }
        self.url = reverse(viewname="auto_labeling_parameter_testing", args=[self.project.item.id])

    @patch("auto_labeling.views.RestAPIRequestTesting.send_request", return_value={})
    def test_called_with_proper_model(self, mock):
        self.assert_create(self.project.admin, status.HTTP_200_OK)
        _, kwargs = mock.call_args
        expected = RequestModelFactory.create(self.data["model_name"], self.data["model_attrs"])
        self.assertEqual(kwargs["model"], expected)

    @patch("auto_labeling.views.RestAPIRequestTesting.send_request", return_value={})
    def test_called_with_text(self, mock):
        self.assert_create(self.project.admin, status.HTTP_200_OK)
        _, kwargs = mock.call_args
        self.assertEqual(kwargs["example"], self.data["text"])

    @patch("auto_labeling.views.RestAPIRequestTesting.send_request", return_value={})
    def test_called_with_image(self, mock):
        self.data["text"] = str(data_dir / "images/1500x500.jpeg")
        self.assert_create(self.project.admin, status.HTTP_200_OK)
        _, kwargs = mock.call_args
        self.assertEqual(kwargs["example"], self.data["text"])


class TestTemplateMapping(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.DOCUMENT_CLASSIFICATION)
        self.data = {
            "response": {
                "Sentiment": "NEUTRAL",
                "SentimentScore": {
                    "Positive": 0.004438233096152544,
                    "Negative": 0.0005306027014739811,
                    "Neutral": 0.9950305223464966,
                    "Mixed": 5.80838445785048e-7,
                },
            },
            "template": AmazonComprehendSentimentTemplate().load(),
            "task_type": "Category",
        }
        self.url = reverse(viewname="auto_labeling_template_test", args=[self.project.item.id])

    def test_template_mapping(self):
        response = self.assert_create(self.project.admin, status.HTTP_200_OK)
        expected = [{"label": "NEUTRAL"}]
        self.assertEqual(response.json(), expected)

    def test_json_decode_error(self):
        self.data["template"] = ""
        self.assert_create(self.project.admin, status.HTTP_400_BAD_REQUEST)


class TestLabelMapping(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.DOCUMENT_CLASSIFICATION)
        self.data = {
            "response": [{"label": "NEGATIVE"}],
            "label_mapping": {"NEGATIVE": "Negative"},
            "task_type": "Category",
        }
        self.url = reverse(viewname="auto_labeling_mapping_test", args=[self.project.item.id])

    def test_label_mapping(self):
        response = self.assert_create(self.project.admin, status.HTTP_200_OK)
        expected = [{"label": "Negative"}]
        self.assertEqual(response.json(), expected)


class TestConfigCreation(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.DOCUMENT_CLASSIFICATION)
        self.data = {
            "model_name": "Amazon Comprehend Sentiment Analysis",
            "model_attrs": {
                "aws_access_key": "str",
                "aws_secret_access_key": "str",
                "region_name": "us-east-1",
                "language_code": "en",
            },
            "template": AmazonComprehendSentimentTemplate().load(),
            "label_mapping": {"NEGATIVE": "Negative"},
            "task_type": "Category",
        }
        self.url = reverse(viewname="auto_labeling_configs", args=[self.project.item.id])

    def test_create_config(self):
        response = self.assert_create(self.project.admin, status.HTTP_201_CREATED)
        self.assertEqual(response.data["model_name"], self.data["model_name"])

    def test_list_config(self):
        mommy.make("AutoLabelingConfig", project=self.project.item)
        response = self.assert_fetch(self.project.admin, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TestAutomatedLabeling(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.DOCUMENT_CLASSIFICATION, single_class_classification=False)
        self.example = make_doc(self.project.item)
        self.category_pos = mommy.make("CategoryType", project=self.project.item, text="POS")
        self.category_neg = mommy.make("CategoryType", project=self.project.item, text="NEG")
        self.loc = mommy.make("SpanType", project=self.project.item, text="LOC")
        self.url = reverse(viewname="auto_labeling", args=[self.project.item.id])
        self.url += f"?example={self.example.id}"

    @patch("auto_labeling.views.execute_pipeline", return_value=Categories([{"label": "POS"}]))
    def test_category_labeling(self, mock):
        mommy.make("AutoLabelingConfig", task_type="Category", project=self.project.item)
        self.assert_create(self.project.admin, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.first().label, self.category_pos)

    @patch("auto_labeling.views.execute_pipeline", return_value=Categories([{"label": "NEUTRAL"}]))
    def test_nonexistent_category(self, mock):
        mommy.make("AutoLabelingConfig", task_type="Category", project=self.project.item)
        self.assert_create(self.project.admin, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 0)

    @patch(
        "auto_labeling.views.execute_pipeline",
        side_effect=[Categories([{"label": "POS"}]), Categories([{"label": "NEG"}])],
    )
    def test_multiple_configs(self, mock):
        mommy.make("AutoLabelingConfig", task_type="Category", project=self.project.item)
        mommy.make("AutoLabelingConfig", task_type="Category", project=self.project.item)
        self.assert_create(self.project.admin, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.first().label, self.category_pos)
        self.assertEqual(Category.objects.last().label, self.category_neg)

    @patch(
        "auto_labeling.views.execute_pipeline",
        side_effect=[Categories([{"label": "POS"}]), Categories([{"label": "POS"}])],
    )
    def test_cannot_label_same_category_type(self, mock):
        mommy.make("AutoLabelingConfig", task_type="Category", project=self.project.item)
        mommy.make("AutoLabelingConfig", task_type="Category", project=self.project.item)
        self.assert_create(self.project.admin, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)

    @patch(
        "auto_labeling.views.execute_pipeline",
        side_effect=[
            Categories([{"label": "POS"}]),
            Spans([{"label": "LOC", "start_offset": 0, "end_offset": 5}]),
        ],
    )
    def test_allow_multi_type_configs(self, mock):
        mommy.make("AutoLabelingConfig", task_type="Category", project=self.project.item)
        mommy.make("AutoLabelingConfig", task_type="Span", project=self.project.item)
        self.assert_create(self.project.admin, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Span.objects.count(), 1)

    @patch("auto_labeling.views.execute_pipeline", return_value=Categories([{"label": "POS"}]))
    def test_cannot_use_other_project_config(self, mock):
        mommy.make("AutoLabelingConfig", task_type="Category")
        self.assert_create(self.project.admin, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 0)


class TestAutomatedSpanLabeling(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.SEQUENCE_LABELING)
        self.example = make_doc(self.project.item)
        self.loc = mommy.make("SpanType", project=self.project.item, text="LOC")
        self.url = reverse(viewname="auto_labeling", args=[self.project.item.id])
        self.url += f"?example={self.example.id}"

    @patch(
        "auto_labeling.views.execute_pipeline",
        side_effect=[
            Spans([{"label": "LOC", "start_offset": 0, "end_offset": 5}]),
            Spans([{"label": "LOC", "start_offset": 4, "end_offset": 10}]),
        ],
    )
    def test_cannot_label_overlapping_span(self, mock):
        mommy.make("AutoLabelingConfig", task_type="Span", project=self.project.item)
        mommy.make("AutoLabelingConfig", task_type="Span", project=self.project.item)
        self.assert_create(self.project.admin, status.HTTP_201_CREATED)
        self.assertEqual(Span.objects.count(), 1)


class TestAutomatedTextLabeling(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.SEQ2SEQ)
        self.example = make_doc(self.project.item)
        self.url = reverse(viewname="auto_labeling", args=[self.project.item.id])
        self.url += f"?example={self.example.id}"

    @patch("auto_labeling.views.execute_pipeline", side_effect=[Texts([{"text": "foo"}]), Texts([{"text": "foo"}])])
    def test_cannot_label_same_text(self, mock):
        mommy.make("AutoLabelingConfig", task_type="Text", project=self.project.item)
        mommy.make("AutoLabelingConfig", task_type="Text", project=self.project.item)
        self.assert_create(self.project.admin, status.HTTP_201_CREATED)
        self.assertEqual(TextLabel.objects.count(), 1)
