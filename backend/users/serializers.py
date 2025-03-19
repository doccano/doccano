from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    sex = serializers.CharField(source='userprofile.sex', read_only=True)
    age = serializers.IntegerField(source='userprofile.age', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'is_superuser', 'sex', 'age')