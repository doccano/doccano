from rest_framework import serializers

from .models import Label, Project, Document, Annotation


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'created_at', 'updated_at', 'users')


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
    project = ProjectSerializer()
    annotations = AnnotationSerializer(many=True)

    class Meta:
        model = Document
        fields = ('id', 'text', 'project', 'annotations')
