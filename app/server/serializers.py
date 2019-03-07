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
        project = instance.project
        model = project.get_annotation_class()
        serializer = project.get_annotation_serializer()
        annotations = model.objects.filter(document=instance.id)
        if request:
            annotations = annotations.filter(user=request.user)
        serializer = serializer(annotations, many=True)
        return serializer.data

    class Meta:
        model = Document
        fields = ('id', 'text', 'annotations', 'meta')


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'guideline', 'users', 'project_type', 'image', 'updated_at')
        read_only_fields = ('image', 'updated_at')


class TextClassificationProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = TextClassificationProject
        fields = ('id', 'name', 'description', 'guideline', 'users', 'project_type', 'image', 'updated_at')
        read_only_fields = ('image', 'updated_at', 'users')


class SequenceLabelingProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = SequenceLabelingProject
        fields = ('id', 'name', 'description', 'guideline', 'users', 'project_type', 'image', 'updated_at')
        read_only_fields = ('image', 'updated_at', 'users')


class Seq2seqProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seq2seqProject
        fields = ('id', 'name', 'description', 'guideline', 'users', 'project_type', 'image', 'updated_at')
        read_only_fields = ('image', 'updated_at', 'users')


class ProjectPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Project: ProjectSerializer,
        TextClassificationProject: TextClassificationProjectSerializer,
        SequenceLabelingProject: SequenceLabelingProjectSerializer,
        Seq2seqProject: Seq2seqProjectSerializer
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
        fields = ('id', 'prob', 'label', 'user')
        read_only_fields = ('user', )

    def create(self, validated_data):
        annotation = DocumentAnnotation.objects.create(**validated_data)
        return annotation


class SequenceAnnotationSerializer(serializers.ModelSerializer):
    #label = ProjectFilteredPrimaryKeyRelatedField(queryset=Label.objects.all())
    label = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all())

    class Meta:
        model = SequenceAnnotation
        fields = ('id', 'prob', 'label', 'start_offset', 'end_offset', 'user')
        read_only_fields = ('user',)

    def create(self, validated_data):
        annotation = SequenceAnnotation.objects.create(**validated_data)
        return annotation


class Seq2seqAnnotationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seq2seqAnnotation
        fields = ('id', 'text', 'user')
        read_only_fields = ('user',)
