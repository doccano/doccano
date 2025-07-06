from rest_framework import serializers
from django.contrib.auth.models import Group, Permission, ContentType

class GroupSerializer(serializers.ModelSerializer):
    permission_names = serializers.SerializerMethodField()
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Permission.objects.all(),
        required=False
    )
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions', 'permission_names']
    
    def get_permission_names(self, obj):
        # Create a dictionary mapping permission IDs to their display names
        permissions_dict = {}
        for permission in Permission.objects.filter(group=obj):
            permissions_dict[permission.id] = {
                'name': permission.name,
                'codename': permission.codename,
                'content_type': permission.content_type.app_label + '.' + permission.content_type.model
            }
        return permissions_dict

class PermissionSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    
    class Meta:
        model = Permission
        fields = '__all__'
    
    def get_label(self, obj):
        if obj.content_type:
            return f"{obj.content_type.app_label} | {obj.content_type.model} | {obj.name}"
        return obj.name

class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'
