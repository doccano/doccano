from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from mixer.backend.django import mixer


class TestProject(TestCase):

    def test_project_type(self):
        project = mixer.blend('server.Project')
        project.is_type_of(project.project_type)

    def test_get_progress(self):
        project = mixer.blend('server.Project')
        res = project.get_progress()
        self.assertEqual(res['total'], 0)
        self.assertEqual(res['remaining'], 0)


class TestLabel(TestCase):

    def test_shortcut_uniqueness(self):
        label = mixer.blend('server.Label')
        mixer.blend('server.Label', shortcut=label.shortcut)
        with self.assertRaises(IntegrityError):
            mixer.blend('server.Label',
                        project=label.project,
                        shortcut=label.shortcut)

    def test_text_uniqueness(self):
        label = mixer.blend('server.Label')
        mixer.blend('server.Label', text=label.text)
        with self.assertRaises(IntegrityError):
            mixer.blend('server.Label',
                        project=label.project,
                        text=label.text)


class TestDocumentAnnotation(TestCase):

    def test_uniqueness(self):
        annotation1 = mixer.blend('server.DocumentAnnotation')
        with self.assertRaises(IntegrityError):
            mixer.blend('server.DocumentAnnotation',
                        document=annotation1.document,
                        user=annotation1.user,
                        label=annotation1.label)


class TestSequenceAnnotation(TestCase):

    def test_uniqueness(self):
        annotation1 = mixer.blend('server.SequenceAnnotation')
        with self.assertRaises(IntegrityError):
            mixer.blend('server.SequenceAnnotation',
                        document=annotation1.document,
                        user=annotation1.user,
                        label=annotation1.label,
                        start_offset=annotation1.start_offset,
                        end_offset=annotation1.end_offset)

    def test_position_constraint(self):
        with self.assertRaises(ValidationError):
            mixer.blend('server.SequenceAnnotation',
                        start_offset=1, end_offset=0).clean()


class TestSeq2seqAnnotation(TestCase):

    def test_uniqueness(self):
        annotation1 = mixer.blend('server.Seq2seqAnnotation')
        with self.assertRaises(IntegrityError):
            mixer.blend('server.Seq2seqAnnotation',
                        document=annotation1.document,
                        user=annotation1.user,
                        text=annotation1.text)
