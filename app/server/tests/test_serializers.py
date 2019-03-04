from django.test import TestCase
from mixer.backend.django import mixer
from ..serializers import LabelSerializer
from ..serializers import Seq2seqAnnotationSerializer


class TestLabelSerializer(TestCase):

    def test_create(self):
        label = mixer.blend('server.Label')
        serializer = LabelSerializer(label)
        self.assertIsInstance(serializer.data, dict)

    def test_annotation(self):
        from rest_framework import serializers
        from ..models import Seq2seqDocument
        class HogeSerializer(serializers.ModelSerializer):
            seq2seq_annotations = Seq2seqAnnotationSerializer(many=True)

            class Meta:
                model = Seq2seqDocument
                fields = ('id', 'text', 'seq2seq_annotations')

        doc = mixer.blend('server.Seq2seqDocument')
        ann = mixer.blend('server.Seq2seqAnnotation')
        doc.seq2seq_annotations.add(ann)
        serializer = HogeSerializer(doc)
        print(serializer.data)
