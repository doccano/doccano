from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    groups_details = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "is_staff", "is_superuser", "is_active", "groups", "groups_details")
    
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
    
    def validate_email(self, value):
        """
        Validate that the email is unique, excluding the current user instance.
        """
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(email=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("Este email já está sendo usado por outro usuário. Por favor, escolha um email diferente.")
        return value


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')

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
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        
        return user