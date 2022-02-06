from auto_labeling_pipeline.models import RequestModelFactory
from rest_framework import serializers

from .models import AutoLabelingConfig


class AutoLabelingConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoLabelingConfig
        fields = ("id", "model_name", "model_attrs", "template", "label_mapping", "default", "task_type")
        read_only_fields = ("created_at", "updated_at")

    def validate_model_name(self, value):
        try:
            RequestModelFactory.find(value)
        except NameError:
            raise serializers.ValidationError(f"The specified model name {value} does not exist.")
        return value

    def valid_label_mapping(self, value):
        if isinstance(value, dict):
            return value
        else:
            raise serializers.ValidationError(f"The {value} is not a dictionary. Please specify it as a dictionary.")

    def validate(self, data):
        try:
            RequestModelFactory.create(data["model_name"], data["model_attrs"])
        except Exception:
            model = RequestModelFactory.find(data["model_name"])
            schema = model.schema()
            required_fields = ", ".join(schema["required"]) if "required" in schema else ""
            raise serializers.ValidationError(
                "The attributes does not match the model."
                "You need to correctly specify the required fields: {}".format(required_fields)
            )
        return data
