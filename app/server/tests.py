from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from mixer.backend.django import mixer


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
