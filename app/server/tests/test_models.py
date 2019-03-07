from django.test import TestCase
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError
from model_mommy import mommy

from ..models import Label, DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation
from ..serializers import DocumentAnnotationSerializer
from ..serializers import SequenceAnnotationSerializer
from ..serializers import Seq2seqAnnotationSerializer


class TestTextClassificationProject(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = mommy.make('server.TextClassificationProject')

    def test_image(self):
        image_url = self.project.image
        self.assertTrue(image_url.endswith('.jpg'))

    def test_get_template_name(self):
        template = self.project.get_template_name()
        self.assertEqual(template, 'annotation/document_classification.html')

    def test_get_annotation_serializer(self):
        serializer = self.project.get_annotation_serializer()
        self.assertEqual(serializer, DocumentAnnotationSerializer)

    def test_get_annotation_class(self):
        klass = self.project.get_annotation_class()
        self.assertEqual(klass, DocumentAnnotation)


class TestSequenceLabelingProject(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = mommy.make('server.SequenceLabelingProject')

    def test_image(self):
        image_url = self.project.image
        self.assertTrue(image_url.endswith('.jpg'))

    def test_get_template_name(self):
        template = self.project.get_template_name()
        self.assertEqual(template, 'annotation/sequence_labeling.html')

    def test_get_annotation_serializer(self):
        serializer = self.project.get_annotation_serializer()
        self.assertEqual(serializer, SequenceAnnotationSerializer)

    def test_get_annotation_class(self):
        klass = self.project.get_annotation_class()
        self.assertEqual(klass, SequenceAnnotation)


class TestSeq2seqProject(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = mommy.make('server.Seq2seqProject')

    def test_image(self):
        image_url = self.project.image
        self.assertTrue(image_url.endswith('.jpg'))

    def test_get_template_name(self):
        template = self.project.get_template_name()
        self.assertEqual(template, 'annotation/seq2seq.html')

    def test_get_annotation_serializer(self):
        serializer = self.project.get_annotation_serializer()
        self.assertEqual(serializer, Seq2seqAnnotationSerializer)

    def test_get_annotation_class(self):
        klass = self.project.get_annotation_class()
        self.assertEqual(klass, Seq2seqAnnotation)


class TestLabel(TestCase):

    def test_shortcut_uniqueness(self):
        label = mommy.make('server.Label', shortcut='a')
        mommy.make('server.Label', shortcut=label.shortcut)
        with self.assertRaises(IntegrityError):
            Label(project=label.project, shortcut=label.shortcut).save()

    def test_create_none_shortcut(self):
        label = mommy.make('server.Label', shortcut=None)
        self.assertEqual(label.shortcut, None)

    def test_text_uniqueness(self):
        label = mommy.make('server.Label')
        mommy.make('server.Label', text=label.text)
        with self.assertRaises(IntegrityError):
            Label(project=label.project, text=label.text).save()


class TestDocumentAnnotation(TestCase):

    def test_uniqueness(self):
        a = mommy.make('server.DocumentAnnotation')
        with self.assertRaises(IntegrityError):
            DocumentAnnotation(document=a.document, user=a.user, label=a.label).save()


class TestSequenceAnnotation(TestCase):

    def test_uniqueness(self):
        a = mommy.make('server.SequenceAnnotation')
        with self.assertRaises(IntegrityError):
            SequenceAnnotation(document=a.document,
                               user=a.user,
                               label=a.label,
                               start_offset=a.start_offset,
                               end_offset=a.end_offset).save()

    def test_position_constraint(self):
        with self.assertRaises(ValidationError):
            mommy.make('server.SequenceAnnotation',
                        start_offset=1, end_offset=0).clean()


class TestSeq2seqAnnotation(TestCase):

    def test_uniqueness(self):
        a = mommy.make('server.Seq2seqAnnotation')
        with self.assertRaises(IntegrityError):
            Seq2seqAnnotation(document=a.document,
                              user=a.user,
                              text=a.text).save()
