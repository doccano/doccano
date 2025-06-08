from rest_framework import viewsets, permissions
from .models import Discussion, ChatMessage
from .serializers import DiscussionSerializer, ChatMessageSerializer
from projects.models import Project

class DiscussionViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Discussion.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)


class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # opcional: remove paginação

    def get_queryset(self):
        discussion_id = self.kwargs.get('discussion_id')
        return ChatMessage.objects.filter(discussion_id=discussion_id).order_by('timestamp')

    def perform_create(self, serializer):
        discussion = Discussion.objects.get(id=self.kwargs.get('discussion_id'))
        serializer.save(user=self.request.user, discussion=discussion)
