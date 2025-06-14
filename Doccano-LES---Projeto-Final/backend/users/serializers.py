from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    is_superuser = serializers.BooleanField(default=False, required=False)
    is_staff = serializers.BooleanField(default=False, required=False)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Um utilizador com este nome de utilizador já existe.")
        return username

    def validate_email(self, email):
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Um utilizador com este email já existe.")
        return email

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'is_superuser': self.validated_data.get('is_superuser', False),
            'is_staff': self.validated_data.get('is_staff', False),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_superuser",
            "is_staff",
        )
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "is_superuser": {"read_only": True},
            "is_staff": {"read_only": True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)  # Garante que a senha será criptografada

        instance.save()
        return instance
