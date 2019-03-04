from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import Label, Project, Document
from .models import TextClassificationProject, SequenceLabelingProject, Seq2seqProject
from .models import DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ('id', 'text', 'shortcut', 'background_color', 'text_color')


class DocumentSerializer(serializers.ModelSerializer):
    annotations = serializers.SerializerMethodField()

    def get_annotations(self, instance):
        request = self.context.get('request')
        view = self.context.get('view', None)
        if request and view:
            project = get_object_or_404(Project, pk=view.kwargs['project_id'])
            model = project.get_annotation_class()
            serializer = project.get_annotation_serializer()
            annotations = model.objects.filter(user=request.user, document=instance.id)
            serializer = serializer(annotations, many=True)
            return serializer.data

    class Meta:
        model = Document
        fields = ('id', 'text', 'annotations')


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'guideline', 'users', 'project_type', 'image', 'updated_at')
        read_only_fields = ('image', 'updated_at')


class ProjectPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Project: ProjectSerializer,
        TextClassificationProject: ProjectSerializer,
        SequenceLabelingProject: ProjectSerializer,
        Seq2seqProject: ProjectSerializer
    }


class ProjectFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        view = self.context.get('view', None)
        request = self.context.get('request', None)
        queryset = super(ProjectFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset or not view:
            return None
        return queryset.filter(project=view.kwargs['project_id'])


class DocumentAnnotationSerializer(serializers.ModelSerializer):
    # label = ProjectFilteredPrimaryKeyRelatedField(queryset=Label.objects.all())
    label = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all())

    class Meta:
        model = DocumentAnnotation
        fields = ('id', 'prob', 'label')

    def create(self, validated_data):
        annotation = DocumentAnnotation.objects.create(**validated_data)
        return annotation


class SequenceAnnotationSerializer(serializers.ModelSerializer):
    #label = ProjectFilteredPrimaryKeyRelatedField(queryset=Label.objects.all())
    label = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all())

    class Meta:
        model = SequenceAnnotation
        fields = ('id', 'prob', 'label', 'start_offset', 'end_offset')

    def create(self, validated_data):
        annotation = SequenceAnnotation.objects.create(**validated_data)
        return annotation


class Seq2seqAnnotationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seq2seqAnnotation
        fields = ('id', 'text')
