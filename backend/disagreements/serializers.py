from rest_framework import serializers
from .models import Disagreement

class DisagreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disagreement
        fields = '__all__'