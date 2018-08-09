from rest_framework import serializers

from .models import Label, Project, Document
from .models import DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ('id', 'text', 'shortcut', 'background_color', 'text_color')


class TextSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ('id', 'text')


class ProjectFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        view = self.context.get('view', None)
        request = self.context.get('request', None)
        queryset = super(ProjectFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset or not view:
            return None
        return queryset.filter(project=view.kwargs['project_id'])


class DocumentAnnotationSerializer(serializers.ModelSerializer):
    label = ProjectFilteredPrimaryKeyRelatedField(queryset=Label.objects.all())

    class Meta:
        model = DocumentAnnotation
        fields = ('id', 'prob', 'label')

    def create(self, validated_data):
        annotation = DocumentAnnotation.objects.create(**validated_data)
        return annotation


class DocumentSerializer(serializers.ModelSerializer):
    labels = DocumentAnnotationSerializer(source='doc_annotations', many=True)

    class Meta:
        model = Document
        fields = ('id', 'text', 'labels')


class SequenceAnnotationSerializer(serializers.ModelSerializer):
    label = ProjectFilteredPrimaryKeyRelatedField(queryset=Label.objects.all())

    class Meta:
        model = SequenceAnnotation
        fields = ('id', 'prob', 'label', 'start_offset', 'end_offset')

    def create(self, validated_data):
        annotation = SequenceAnnotation.objects.create(**validated_data)
        return annotation


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

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'users', 'project_type', 'image')
