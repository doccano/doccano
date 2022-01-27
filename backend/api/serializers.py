from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import (Comment, Example, ExampleState,
                     ImageClassificationProject,
                     IntentDetectionAndSlotFillingProject, Project,
                     Seq2seqProject, SequenceLabelingProject,
                     Speech2textProject, Tag, TextClassificationProject)


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
