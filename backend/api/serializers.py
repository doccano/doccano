from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import (ImageClassificationProject,
                     IntentDetectionAndSlotFillingProject, Project,
                     Seq2seqProject, SequenceLabelingProject,
                     Speech2textProject, Tag, TextClassificationProject)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'project', 'text', )
        read_only_fields = ('id', 'project')


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
