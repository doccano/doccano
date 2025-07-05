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
        
        # Só permite criar discussões se o projeto estiver fechado
        if project.is_open:
            raise ValueError("Discussões só podem ser criadas quando o projeto está fechado")
        
        serializer.save(project=project)

    def create(self, request, *args, **kwargs):
        """Override para capturar erro de validação"""
        try:
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        """Override para validar estado do projeto"""
        discussion = self.get_object()
        
        # Só permite atualizar discussões se o projeto estiver fechado
        if discussion.project.is_open:
            return Response(
                {'error': 'Discussões só podem ser modificadas quando o projeto está fechado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Override para validar estado do projeto"""
        discussion = self.get_object()
        
        # Só permite deletar discussões se o projeto estiver fechado
        if discussion.project.is_open:
            return Response(
                {'error': 'Discussões só podem ser deletadas quando o projeto está fechado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='close')
    def close_discussion(self, request, project_id=None, pk=None):
        """
        Encerra a discussão atual definindo a data de fim como a data atual.
        """
        discussion = self.get_object()
        
        # Só permite fechar discussões se o projeto estiver fechado
        if discussion.project.is_open:
            return Response(
                {'error': 'Discussões só podem ser fechadas quando o projeto está fechado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
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
        
        # Só permite reabrir discussões se o projeto estiver fechado
        if discussion.project.is_open:
            return Response(
                {'error': 'Discussões só podem ser reabertas quando o projeto está fechado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
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
        
        # Só permite criar mensagens se o projeto estiver fechado
        if discussion.project.is_open:
            raise ValueError("Mensagens só podem ser criadas quando o projeto está fechado")
        
        serializer.save(user=self.request.user, discussion=discussion)

    def create(self, request, *args, **kwargs):
        """Override para capturar erro de validação"""
        try:
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
