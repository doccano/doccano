from rest_framework import serializers

from .models import Category, Relation, Span, TextLabel
from examples.models import Example
from label_types.models import CategoryType, RelationType, SpanType


class CategorySerializer(serializers.ModelSerializer):
    label = serializers.PrimaryKeyRelatedField(queryset=CategoryType.objects.all())
    example = serializers.PrimaryKeyRelatedField(queryset=Example.objects.all())

    class Meta:
        model = Category
        fields = (
            "id",
            "prob",
            "user",
            "example",
            "created_at",
            "updated_at",
            "label",
        )
        read_only_fields = ("user",)


class SpanSerializer(serializers.ModelSerializer):
    label = serializers.PrimaryKeyRelatedField(queryset=SpanType.objects.all())
    example = serializers.PrimaryKeyRelatedField(queryset=Example.objects.all())

    class Meta:
        model = Span
        fields = (
            "id",
            "prob",
            "user",
            "example",
            "created_at",
            "updated_at",
            "label",
            "start_offset",
            "end_offset",
        )
        read_only_fields = ("user",)


class TextLabelSerializer(serializers.ModelSerializer):
    example = serializers.PrimaryKeyRelatedField(queryset=Example.objects.all())

    class Meta:
        model = TextLabel
        fields = (
            "id",
            "prob",
            "user",
            "example",
            "created_at",
            "updated_at",
            "text",
        )
        read_only_fields = ("user",)


class RelationSerializer(serializers.ModelSerializer):
    example = serializers.PrimaryKeyRelatedField(queryset=Example.objects.all())
    type = serializers.PrimaryKeyRelatedField(queryset=RelationType.objects.all())

    class Meta:
        model = Relation
        fields = ("id", "prob", "user", "example", "created_at", "updated_at", "from_id", "to_id", "type")
        read_only_fields = ("user",)
