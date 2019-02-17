from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from mixer.backend.django import mixer
from ..models import Label, DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation


class TestProject(TestCase):

    def test_project_type(self):
        project = mixer.blend('server.Project')
        project.is_type_of(project.project_type)

    def test_get_progress(self):
        project = mixer.blend('server.Project')
        res = project.get_progress(None)
        self.assertEqual(res['total'], 0)
        self.assertEqual(res['remaining'], 0)


class TestLabel(TestCase):

    def test_shortcut_uniqueness(self):
        label = mixer.blend('server.Label', shortcut='a')
        mixer.blend('server.Label', shortcut=label.shortcut)
        with self.assertRaises(IntegrityError):
            Label(project=label.project, shortcut=label.shortcut).save()

    def test_create_none_shortcut(self):
        label = mixer.blend('server.Label', shortcut=None)
        self.assertEqual(label.shortcut, None)

    def test_text_uniqueness(self):
        label = mixer.blend('server.Label')
        mixer.blend('server.Label', text=label.text)
        with self.assertRaises(IntegrityError):
            Label(project=label.project, text=label.text).save()


class TestDocumentAnnotation(TestCase):

    def test_uniqueness(self):
        a = mixer.blend('server.DocumentAnnotation')
        with self.assertRaises(IntegrityError):
            DocumentAnnotation(document=a.document, user=a.user, label=a.label).save()


class TestSequenceAnnotation(TestCase):

    def test_uniqueness(self):
        a = mixer.blend('server.SequenceAnnotation')
        with self.assertRaises(IntegrityError):
            SequenceAnnotation(document=a.document,
                               user=a.user,
                               label=a.label,
                               start_offset=a.start_offset,
                               end_offset=a.end_offset).save()

    def test_position_constraint(self):
        with self.assertRaises(ValidationError):
            mixer.blend('server.SequenceAnnotation',
                        start_offset=1, end_offset=0).clean()


class TestSeq2seqAnnotation(TestCase):

    def test_uniqueness(self):
        a = mixer.blend('server.Seq2seqAnnotation')
        with self.assertRaises(IntegrityError):
            Seq2seqAnnotation(document=a.document,
                              user=a.user,
                              text=a.text).save()
