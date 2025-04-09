from rest_framework import serializers
from .models import Annotation

class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = '__all__'
        read_only_fields = ('annotator', 'created_at', 'updated_at')

    def update(self, instance, validated_data):
        if "extracted_labels" in validated_data:
            instance.extracted_labels = validated_data["extracted_labels"]
        return super().update(instance, validated_data)