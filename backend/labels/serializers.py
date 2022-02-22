from rest_framework import serializers

from .models import Category, RelationNew, Span, TextLabel
from examples.models import Example
from label_types.models import CategoryType, SpanType


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
    def validate(self, attrs):
        return super().validate(attrs)

    class Meta:
        model = RelationNew
        fields = ("id", "prob", "user", "example", "created_at", "updated_at", "from_id", "to_id", "type")
