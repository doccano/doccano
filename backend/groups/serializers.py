from rest_framework import serializers
from .models import Group, GroupPermissions, Permission

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']  # Include only the fields you need

class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
        extra_kwargs = {
            'name': {'required': True}
        }
    def create(self, validated_data):
        group = Group(**validated_data)
        group.save()
        return group
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
    def delete(self, instance):
        instance.delete()
        return instance
    def validate(self, data):
        if 'name' in data and not data['name']:
            raise serializers.ValidationError("Group name cannot be empty.")
        return data

class GroupPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPermissions
        fields = ['id', 'group_id', 'permission_id']  # Include only the fields you need

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'content_type_id', 'codename']  # Include only the fields you need
    extra_kwargs = {
        'name': {'required': True},
        'content_type_id': {'required': True},
        'codename': {'required': True}
    }

class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'ContentType'
        fields = ['id', 'app_label', 'model']  # Include only the fields you need
    extra_kwargs = {
        'app_label': {'required': True},
        'model': {'required': True}
    }