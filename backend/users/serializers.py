from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    groups_details = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "is_superuser", "is_active", "groups", "groups_details")
    
    def get_groups_details(self, obj):
        groups_dict = {}
        for group in obj.groups.all():
            groups_dict[group.id] = {
                'name': group.name
            }
        return groups_dict


class UserDetailSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Group.objects.all(),
        required=False
    )
    groups_details = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "is_superuser", "is_active", 
                 "first_name", "last_name", "date_joined", "groups", "groups_details")
    
    def get_groups_details(self, obj):
        groups_dict = {}
        for group in obj.groups.all():
            groups_dict[group.id] = {
                'name': group.name
            }
        return groups_dict


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Password fields didn't match."})
        
        # Check if email already exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "User with this email already exists."})
            
        return attrs

    def create(self, validated_data):
        # Remove password_confirm as we don't need it to create the user
        validated_data.pop('password_confirm')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        return user