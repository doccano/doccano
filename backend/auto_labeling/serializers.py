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
        # Convert model_attrs from UI format (list of objects) to dict format
        model_attrs = data.get("model_attrs", [])
        attrs_dict = {}

        if isinstance(model_attrs, list):
            # Frontend sends as [{name: "url", value: "..."}, ...]
            for attr in model_attrs:
                if isinstance(attr, dict) and "name" in attr:
                    attrs_dict[attr["name"]] = attr.get("value", "")
        else:
            # Already in dict format
            attrs_dict = model_attrs

        # For CustomRESTRequestModel, provide defaults for optional fields if not present
        if data.get("model_name") == "Custom REST Request":
            if "params" not in attrs_dict:
                attrs_dict["params"] = {}
            if "headers" not in attrs_dict:
                attrs_dict["headers"] = {}
            if "body" not in attrs_dict:
                attrs_dict["body"] = {}

        # Now try to create the model with the populated attributes
        try:
            RequestModelFactory.create(data["model_name"], attrs_dict)
        except Exception as e:
            model = RequestModelFactory.find(data["model_name"])
            schema = model.schema()
            required_fields = ", ".join(schema["required"]) if "required" in schema else ""
            # Include the actual error message for debugging
            error_msg = f"The attributes does not match the model. You need to correctly specify the required fields: {required_fields}. Details: {str(e)}"
            raise serializers.ValidationError(error_msg)
        return data
