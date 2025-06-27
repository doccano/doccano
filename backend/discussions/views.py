

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404 # Garanta que este import está presente

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
        project = get_object_or_404(Project, id=project_id)
        serializer.save(project=project)

    @action(detail=True, methods=['post'], url_path='close')
    def close_discussion(self, request, project_id=None, pk=None):
        """
        Encerra a discussão atual definindo a data de fim como a data atual.
        """
        discussion = self.get_object()
        discussion.end_date = timezone.now().date()
        discussion.save()
        serializer = self.get_serializer(discussion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='reopen')
    def reopen_discussion(self, request, project_id=None, pk=None):
        """
        Reabre uma discussão definindo uma nova data de fim.
        """
        discussion = self.get_object()
        new_end_date = request.data.get('end_date')

        if not new_end_date:
            return Response(
                {'error': 'A nova data de fim (end_date) é obrigatória.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        discussion.end_date = new_end_date
        discussion.save()

        # Retorna a discussão atualizada para o frontend
        serializer = self.get_serializer(discussion)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
