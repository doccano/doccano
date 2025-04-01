from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import (
    Answer,
    BoundingBoxProject,
    ImageCaptioningProject,
    ImageClassificationProject,
    IntentDetectionAndSlotFillingProject,
    Member,
    OptionQuestion,
    OptionsGroup,
    Perspective,
    Project,
    Question,
    QuestionType,
    SegmentationProject,
    Seq2seqProject,
    SequenceLabelingProject,
    Speech2textProject,
    Tag,
    TextClassificationProject,
)


class MemberSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    rolename = serializers.SerializerMethodField()
    perspective_id = serializers.PrimaryKeyRelatedField(
        source="perspective", required=False, queryset=Perspective.objects.all(), allow_null=True
    )

    @classmethod
    def get_username(cls, instance):
        user = instance.user
        return user.username if user else None

    @classmethod
    def get_rolename(cls, instance):
        role = instance.role
        return role.name if role else None

    class Meta:
        model = Member
        fields = ("id", "user", "role", "username", "rolename", "perspective_id")


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = ["id", "question_type"]


class OptionQuestionSerializer(serializers.ModelSerializer):
    options_group = serializers.PrimaryKeyRelatedField(queryset=OptionsGroup.objects.all(), required=False)

    class Meta:
        model = OptionQuestion
        fields = ["id", "option", "options_group"]


class OptionsGroupSerializer(serializers.ModelSerializer):
    options_questions = OptionQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = OptionsGroup
        fields = ["id", "name", "options_questions"]


class AnswerSerializer(serializers.ModelSerializer):
    member = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all())
    answer_option = serializers.PrimaryKeyRelatedField(queryset=OptionQuestion.objects.all(), required=False)
    answer_text = serializers.CharField(required=False)

    class Meta:
        model = Answer
        fields = ("id", "question", "member", "answer_text", "answer_option")

    def validate(self, attrs):
        answer_text = attrs.get("answer_text", None)
        answer_option = attrs.get("answer_option", None)

        if answer_text and answer_option:
            raise serializers.ValidationError(
                "You can only provide one of the fiels: 'answer_text' or 'answer_option', but not both."
            )

        if not answer_text and not answer_option:
            raise serializers.ValidationError(
                "You must provide at least one of the fields: 'answer_text' or 'answer_option'."
            )

        return attrs


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    perspective = serializers.PrimaryKeyRelatedField(
        queryset=Perspective.objects.all(), write_only=True, required=False
    )
    type = serializers.PrimaryKeyRelatedField(queryset=QuestionType.objects.all())
    options_group = serializers.PrimaryKeyRelatedField(queryset=OptionsGroup.objects.all(), required=False)

    class Meta:
        model = Question
        fields = ("id", "question", "perspective", "answers", "type", "options_group")


class PerspectiveSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=Member.objects.filter(role__name="annotator"), many=True)
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source="project",
    )
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Perspective
        fields = ("id", "project_id", "created_at", "members", "questions")
        read_only_fields = ("created_at",)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "project",
            "text",
        )
        read_only_fields = ("id", "project")


class AnswerNestedSerializer(serializers.ModelSerializer):
    member = serializers.StringRelatedField()

    class Meta:
        model = Answer
        fields = ("id", "answer", "member")


class QuestionNestedSerializer(serializers.ModelSerializer):
    answers = AnswerNestedSerializer(many=True, read_only=True, source="answers")

    class Meta:
        model = Question
        fields = ("id", "question", "answers")


class PerspectiveNestedSerializer(serializers.ModelSerializer):
    questions = QuestionNestedSerializer(many=True, read_only=True, source="questions")

    class Meta:
        model = Perspective
        fields = ("id", "created_at", "questions")


class ProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    author = serializers.SerializerMethodField()
    perspectives = PerspectiveNestedSerializer(many=True, read_only=True)

    @classmethod
    def get_author(cls, instance):
        if instance.created_by:
            return instance.created_by.username
        return ""

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "guideline",
            "project_type",
            "created_at",
            "updated_at",
            "random_order",
            "author",
            "collaborative_annotation",
            "single_class_classification",
            "allow_member_to_create_label_type",
            "is_text_project",
            "tags",
            "perspectives",
        ]
        read_only_fields = (
            "created_at",
            "updated_at",
            "author",
            "is_text_project",
        )

    def create(self, validated_data):
        tags = TagSerializer(data=validated_data.pop("tags", []), many=True)
        project = self.Meta.model.objects.create(**validated_data)
        tags.is_valid()
        tags.save(project=project)
        return project

    def update(self, instance, validated_data):
        # Don't update tags. Please use TagAPI.
        validated_data.pop("tags", None)
        return super().update(instance, validated_data)


class TextClassificationProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        model = TextClassificationProject


class SequenceLabelingProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        model = SequenceLabelingProject
        fields = ProjectSerializer.Meta.fields + ["allow_overlapping", "grapheme_mode", "use_relation"]


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


class BoundingBoxProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        model = BoundingBoxProject


class SegmentationProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        model = SegmentationProject


class ImageCaptioningProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        model = ImageCaptioningProject


class ProjectPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Project: ProjectSerializer,
        **{cls.Meta.model: cls for cls in ProjectSerializer.__subclasses__()},
    }
