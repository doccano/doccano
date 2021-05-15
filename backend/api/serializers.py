from auto_labeling_pipeline.models import RequestModelFactory
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import (DOCUMENT_CLASSIFICATION, IMAGE_CLASSIFICATION, SEQ2SEQ,
                     SEQUENCE_LABELING, SPEECH2TEXT, AutoLabelingConfig,
                     Category, Comment, Example, ImageClassificationProject,
                     Label, Project, Role, RoleMapping, Seq2seqProject,
                     SequenceLabelingProject, Span, Speech2textProject, Tag,
                     TextClassificationProject, TextLabel)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'is_superuser')


class LabelSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        prefix_key = attrs.get('prefix_key')
        suffix_key = attrs.get('suffix_key')

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
            label_id = context['kwargs'].get('label_id')
        except (AttributeError, KeyError):
            pass  # unit tests don't always have the correct context set up
        else:
            conflicting_labels = Label.objects.filter(
                suffix_key=suffix_key,
                prefix_key=prefix_key,
                project=project_id,
            )

            if label_id is not None:
                conflicting_labels = conflicting_labels.exclude(id=label_id)

            if conflicting_labels.exists():
                raise ValidationError('Duplicate shortcut key.')

        return super().validate(attrs)

    class Meta:
        model = Label
        fields = ('id', 'text', 'prefix_key', 'suffix_key', 'background_color', 'text_color')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'user', 'username', 'example', 'text', 'created_at', )
        read_only_fields = ('user', 'example')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'project', 'text', )
        read_only_fields = ('id', 'project')


class ExampleSerializer(serializers.ModelSerializer):
    annotations = serializers.SerializerMethodField()
    annotation_approver = serializers.SerializerMethodField()

    def get_annotations(self, instance):
        request = self.context.get('request')
        project = instance.project
        model = project.get_annotation_class()
        serializer = get_annotation_serializer(task=project.project_type)
        annotations = model.objects.filter(example=instance.id)
        if request and not project.collaborative_annotation:
            annotations = annotations.filter(user=request.user)
        serializer = serializer(annotations, many=True)
        return serializer.data

    @classmethod
    def get_annotation_approver(cls, instance):
        approver = instance.annotations_approved_by
        return approver.username if approver else None

    class Meta:
        model = Example
        fields = [
            'id',
            'filename',
            'annotations',
            'meta',
            'annotation_approver',
            'comment_count',
            'text'
        ]
        read_only_fields = ['filename']


class ApproverSerializer(ExampleSerializer):

    class Meta:
        model = Example
        fields = ('id', 'annotation_approver')


class ProjectSerializer(serializers.ModelSerializer):
    current_users_role = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, required=False)

    def get_current_users_role(self, instance):
        role_abstractor = {
            "is_project_admin": settings.ROLE_PROJECT_ADMIN,
            "is_annotator": settings.ROLE_ANNOTATOR,
            "is_annotation_approver": settings.ROLE_ANNOTATION_APPROVER,
        }
        queryset = RoleMapping.objects.values("role_id__name")
        if queryset:
            users_role = get_object_or_404(
                queryset, project=instance.id, user=self.context.get("request").user.id
            )
            for key, val in role_abstractor.items():
                role_abstractor[key] = users_role["role_id__name"] == val
        return role_abstractor

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'description',
            'guideline',
            'users',
            'current_users_role',
            'project_type',
            'updated_at',
            'random_order',
            'collaborative_annotation',
            'single_class_classification',
            'tags'
        )
        read_only_fields = (
            'updated_at',
            'users',
            'current_users_role',
            'tags'
        )


class TextClassificationProjectSerializer(ProjectSerializer):

    class Meta(ProjectSerializer.Meta):
        model = TextClassificationProject


class SequenceLabelingProjectSerializer(ProjectSerializer):

    class Meta(ProjectSerializer.Meta):
        model = SequenceLabelingProject


class Seq2seqProjectSerializer(ProjectSerializer):

    class Meta(ProjectSerializer.Meta):
        model = Seq2seqProject


class Speech2textProjectSerializer(ProjectSerializer):

    class Meta(ProjectSerializer.Meta):
        model = Speech2textProject


class ImageClassificationProjectSerializer(ProjectSerializer):

    class Meta(ProjectSerializer.Meta):
        model = ImageClassificationProject


class ProjectPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Project: ProjectSerializer,
        **{
            cls.Meta.model: cls for cls in ProjectSerializer.__subclasses__()
        }
    }


class CategorySerializer(serializers.ModelSerializer):
    label = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all())
    example = serializers.PrimaryKeyRelatedField(queryset=Example.objects.all())

    class Meta:
        model = Category
        fields = (
            'id',
            'prob',
            'user',
            'example',
            'created_at',
            'updated_at',
            'label',
        )
        read_only_fields = ('user',)


class SpanSerializer(serializers.ModelSerializer):
    label = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all())
    example = serializers.PrimaryKeyRelatedField(queryset=Example.objects.all())

    class Meta:
        model = Span
        fields = (
            'id',
            'prob',
            'user',
            'example',
            'created_at',
            'updated_at',
            'label',
            'start_offset',
            'end_offset',
        )
        read_only_fields = ('user',)


class TextLabelSerializer(serializers.ModelSerializer):
    example = serializers.PrimaryKeyRelatedField(queryset=Example.objects.all())

    class Meta:
        model = TextLabel
        fields = (
            'id',
            'prob',
            'user',
            'example',
            'created_at',
            'updated_at',
            'text',
        )
        read_only_fields = ('user',)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')


class RoleMappingSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    rolename = serializers.SerializerMethodField()

    @classmethod
    def get_username(cls, instance):
        user = instance.user
        return user.username if user else None

    @classmethod
    def get_rolename(cls, instance):
        role = instance.role
        return role.name if role else None

    class Meta:
        model = RoleMapping
        fields = ('id', 'user', 'role', 'username', 'rolename')


class AutoLabelingConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = AutoLabelingConfig
        fields = ('id', 'model_name', 'model_attrs', 'template', 'label_mapping', 'default')
        read_only_fields = ('created_at', 'updated_at')

    def validate_model_name(self, value):
        try:
            RequestModelFactory.find(value)
        except NameError:
            raise serializers.ValidationError(f'The specified model name {value} does not exist.')
        return value

    def valid_label_mapping(self, value):
        if isinstance(value, dict):
            return value
        else:
            raise serializers.ValidationError(f'The {value} is not a dictionary. Please specify it as a dictionary.')

    def validate(self, data):
        try:
            RequestModelFactory.create(data['model_name'], data['model_attrs'])
        except Exception:
            model = RequestModelFactory.find(data['model_name'])
            schema = model.schema()
            required_fields = ', '.join(schema['required']) if 'required' in schema else ''
            raise serializers.ValidationError(
                'The attributes does not match the model.'
                'You need to correctly specify the required fields: {}'.format(required_fields)
            )
        return data


def get_annotation_serializer(task: str):
    mapping = {
        DOCUMENT_CLASSIFICATION: CategorySerializer,
        SEQUENCE_LABELING: SpanSerializer,
        SEQ2SEQ: TextLabelSerializer,
        SPEECH2TEXT: TextLabelSerializer,
        IMAGE_CLASSIFICATION: CategorySerializer,
    }
    try:
        return mapping[task]
    except KeyError:
        raise ValueError(f'{task} is not implemented.')
