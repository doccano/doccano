from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from rest_framework.exceptions import ValidationError


from .models import Label, Project, Document
from .models import TextClassificationProject, SequenceLabelingProject, Seq2seqProject
from .models import DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_superuser')


class LabelSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if 'prefix_key' not in attrs and 'suffix_key' not in attrs:
            return super().validate(attrs)

        prefix_key = attrs['prefix_key']
        suffix_key = attrs['suffix_key']

        # In the case of user don't set any shortcut key.
        if prefix_key is None and suffix_key is None:
            return super().validate(attrs)

        # Don't allow shortcut key not to have a suffix key.
        if prefix_key and not suffix_key:
            raise ValidationError('Shortcut key may not have a suffix key.')

        # Don't allow to save same shortcut key when prefix_key is null.
        try:
            context = self.context['request'].parser_context
            project_id = context['kwargs']['project_id']
        except (AttributeError, KeyError):
            pass  # unit tests don't always have the correct context set up
        else:
            if Label.objects.filter(suffix_key=suffix_key,
                                    prefix_key__isnull=True,
                                    project=project_id).exists():
                raise ValidationError('Duplicate key.')

        return super().validate(attrs)

    class Meta:
        model = Label
        fields = ('id', 'text', 'prefix_key', 'suffix_key', 'background_color', 'text_color')


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
        fields = ('id', 'name', 'description', 'guideline', 'users', 'project_type', 'image', 'updated_at',
                  'randomize_document_order')
        read_only_fields = ('image', 'updated_at')


class TextClassificationProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = TextClassificationProject
        fields = ('id', 'name', 'description', 'guideline', 'users', 'project_type', 'image', 'updated_at',
                  'randomize_document_order')
        read_only_fields = ('image', 'updated_at', 'users')


class SequenceLabelingProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = SequenceLabelingProject
        fields = ('id', 'name', 'description', 'guideline', 'users', 'project_type', 'image', 'updated_at',
                  'randomize_document_order')
        read_only_fields = ('image', 'updated_at', 'users')


class Seq2seqProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seq2seqProject
        fields = ('id', 'name', 'description', 'guideline', 'users', 'project_type', 'image', 'updated_at',
                  'randomize_document_order')
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
    document = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())

    class Meta:
        model = DocumentAnnotation
        fields = ('id', 'prob', 'label', 'user', 'document')
        read_only_fields = ('user', )


class SequenceAnnotationSerializer(serializers.ModelSerializer):
    #label = ProjectFilteredPrimaryKeyRelatedField(queryset=Label.objects.all())
    label = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all())
    document = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())

    class Meta:
        model = SequenceAnnotation
        fields = ('id', 'prob', 'label', 'start_offset', 'end_offset', 'user', 'document')
        read_only_fields = ('user',)


class Seq2seqAnnotationSerializer(serializers.ModelSerializer):
    document = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())

    class Meta:
        model = Seq2seqAnnotation
        fields = ('id', 'text', 'user', 'document')
        read_only_fields = ('user',)
