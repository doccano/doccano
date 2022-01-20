from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import (AnnotationRelations, Category, CategoryType, Comment,
                     Example, ExampleState, ImageClassificationProject,
                     IntentDetectionAndSlotFillingProject, Label, Project,
                     RelationTypes, Seq2seqProject, SequenceLabelingProject,
                     Span, SpanType, Speech2textProject, Tag,
                     TextClassificationProject, TextLabel)


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
            conflicting_labels = self.Meta.model.objects.filter(
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
        fields = (
            'id',
            'text',
            'prefix_key',
            'suffix_key',
            'background_color',
            'text_color',
        )


class CategoryTypeSerializer(LabelSerializer):
    class Meta:
        model = CategoryType
        fields = (
            'id',
            'text',
            'prefix_key',
            'suffix_key',
            'background_color',
            'text_color',
        )


class SpanTypeSerializer(LabelSerializer):
    class Meta:
        model = SpanType
        fields = (
            'id',
            'text',
            'prefix_key',
            'suffix_key',
            'background_color',
            'text_color',
        )


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
    annotation_approver = serializers.SerializerMethodField()
    is_confirmed = serializers.SerializerMethodField()

    @classmethod
    def get_annotation_approver(cls, instance):
        approver = instance.annotations_approved_by
        return approver.username if approver else None

    def get_is_confirmed(self, instance):
        user = self.context.get('request').user
        if instance.project.collaborative_annotation:
            states = instance.states.all()
        else:
            states = instance.states.filter(confirmed_by_id=user.id)
        return states.count() > 0

    class Meta:
        model = Example
        fields = [
            'id',
            'filename',
            'meta',
            'annotation_approver',
            'comment_count',
            'text',
            'is_confirmed'
        ]
        read_only_fields = ['filename', 'is_confirmed']


class ExampleStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExampleState
        fields = ('id', 'example', 'confirmed_by')
        read_only_fields = ('id', 'example', 'confirmed_by')


class ApproverSerializer(ExampleSerializer):

    class Meta:
        model = Example
        fields = ('id', 'annotation_approver')


class ProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'description',
            'guideline',
            'project_type',
            'updated_at',
            'random_order',
            'created_by',
            'collaborative_annotation',
            'single_class_classification',
            'is_text_project',
            'can_define_label',
            'can_define_relation',
            'can_define_category',
            'can_define_span',
            'tags'
        )
        read_only_fields = (
            'updated_at',
            'is_text_project',
            'can_define_label',
            'can_define_relation',
            'can_define_category',
            'can_define_span',
            'tags'
        )


class TextClassificationProjectSerializer(ProjectSerializer):

    class Meta(ProjectSerializer.Meta):
        model = TextClassificationProject


class SequenceLabelingProjectSerializer(ProjectSerializer):

    class Meta(ProjectSerializer.Meta):
        model = SequenceLabelingProject
        fields = ProjectSerializer.Meta.fields + ('allow_overlapping', 'grapheme_mode')


class Seq2seqProjectSerializer(ProjectSerializer):

    class Meta(ProjectSerializer.Meta):
        model = Seq2seqProject


class IntentDetectionAndSlotFillingProjectSerializer(ProjectSerializer):

    class Meta(ProjectSerializer.Meta):
        model = IntentDetectionAndSlotFillingProject


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
    label = serializers.PrimaryKeyRelatedField(queryset=CategoryType.objects.all())
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
    label = serializers.PrimaryKeyRelatedField(queryset=SpanType.objects.all())
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


class RelationTypesSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        return super().validate(attrs)

    class Meta:
        model = RelationTypes
        fields = ('id', 'color', 'name')


class AnnotationRelationsSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        return super().validate(attrs)

    class Meta:
        model = AnnotationRelations
        fields = ('id', 'annotation_id_1', 'annotation_id_2', 'type', 'user', 'timestamp')
