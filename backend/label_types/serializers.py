from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CategoryType, LabelType, RelationType, SpanType


class LabelSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        prefix_key = attrs.get("prefix_key")
        suffix_key = attrs.get("suffix_key")

        # In the case of user don't set any shortcut key.
        if prefix_key is None and suffix_key is None:
            return super().validate(attrs)

        # Don't allow shortcut key not to have a suffix key.
        if prefix_key and not suffix_key:
            raise ValidationError("Shortcut key may not have a suffix key.")

        # Don't allow to save same shortcut key when prefix_key is null.
        try:
            context = self.context["request"].parser_context
            project_id = context["kwargs"]["project_id"]
            label_id = context["kwargs"].get("label_id")
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
                raise ValidationError("Duplicate shortcut key.")

        return super().validate(attrs)

    class Meta:
        model = LabelType
        fields = (
            "id",
            "text",
            "prefix_key",
            "suffix_key",
            "background_color",
            "text_color",
        )


class CategoryTypeSerializer(LabelSerializer):
    class Meta:
        model = CategoryType
        fields = LabelSerializer.Meta.fields


class SpanTypeSerializer(LabelSerializer):
    class Meta:
        model = SpanType
        fields = LabelSerializer.Meta.fields


class RelationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationType
        fields = LabelSerializer.Meta.fields
