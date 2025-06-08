from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Discussion, ChatMessage

class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = ['id', 'project', 'title', 'start_date', 'end_date']
        read_only_fields = ['project']


class ChatMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    userId = serializers.IntegerField(source='user.id', read_only=True)  # ADICIONE ISSO

    class Meta:
        model = ChatMessage
        fields = ['id', 'discussion', 'user', 'userId', 'username', 'text', 'timestamp']
        read_only_fields = ['id', 'user', 'userId', 'username', 'timestamp', 'discussion']
