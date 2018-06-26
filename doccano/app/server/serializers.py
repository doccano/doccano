from rest_framework import serializers

from .models import Label, Project, Document, Annotation


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ('id', 'text', 'shortcut')


class AnnotationSerializer(serializers.ModelSerializer):
    label = LabelSerializer()

    class Meta:
        model = Annotation
        fields = ('id', 'prob', 'label')


class DocumentSerializer(serializers.ModelSerializer):
    labels = AnnotationSerializer(many=True)

    class Meta:
        model = Document
        fields = ('id', 'text', 'labels')


class ProjectSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True)
    documents = DocumentSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'users', 'labels', 'documents')
