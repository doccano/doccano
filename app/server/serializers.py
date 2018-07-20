from rest_framework import serializers

from .models import Label, Project, Document
from .models import DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ('id', 'text', 'shortcut', 'background_color', 'text_color')


class DocumentAnnotationSerializer(serializers.ModelSerializer):
    label = LabelSerializer()

    class Meta:
        model = DocumentAnnotation
        fields = ('id', 'prob', 'label')


class DocumentSerializer(serializers.ModelSerializer):
    labels = DocumentAnnotationSerializer(source='doc_annotations', many=True)

    class Meta:
        model = Document
        fields = ('id', 'text', 'labels')


class SequenceAnnotationSerializer(serializers.ModelSerializer):
    label = LabelSerializer()

    class Meta:
        model = SequenceAnnotation
        fields = ('id', 'prob', 'label', 'start_offset', 'end_offset')


class SequenceSerializer(serializers.ModelSerializer):
    labels = SequenceAnnotationSerializer(source='seq_annotations', many=True)

    class Meta:
        model = Document
        fields = ('id', 'text', 'labels')


class Seq2seqAnnotationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seq2seqAnnotation
        fields = ('id', 'text')


class Seq2seqSerializer(serializers.ModelSerializer):
    labels = Seq2seqAnnotationSerializer(source='seq2seq_annotations', many=True)

    class Meta:
        model = Document
        fields = ('id', 'text', 'labels')


class ProjectSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True)
    documents = DocumentSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'users', 'labels', 'documents')
