from rest_framework import serializers

from .models import Label, Project, Document
from .models import DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ('id', 'text', 'shortcut')


class DocumentAnnotationSerializer(serializers.ModelSerializer):
    label = LabelSerializer()

    class Meta:
        model = DocumentAnnotation
        fields = ('id', 'prob', 'label')


class DocumentSerializer(serializers.ModelSerializer):
    doc_annotations = DocumentAnnotationSerializer(many=True)

    class Meta:
        model = Document
        fields = ('id', 'text', 'doc_annotations')


class ProjectSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True)
    documents = DocumentSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'users', 'labels', 'documents')
