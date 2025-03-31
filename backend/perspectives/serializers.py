from rest_framework import serializers
from .models import Perspective

class PerspectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perspective
        fields = '__all__'
        extra_kwargs = {
            'linkedAnnotations': {'read_only': False},
        }