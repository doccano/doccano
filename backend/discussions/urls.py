from django.urls import path
from .views import DiscussionViewSet, ChatMessageViewSet

# Endpoints de discussões
discussion_list = DiscussionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

discussion_detail = DiscussionViewSet.as_view({
    'get': 'retrieve'
})

# Endpoints de mensagens no chat de uma discussão
chat_list = ChatMessageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    # Discussões por projeto
    path('projects/<int:project_id>/discussions/', discussion_list, name='discussion-list'),
    path('projects/<int:project_id>/discussions/<int:pk>/', discussion_detail, name='discussion-detail'),

    # Chat da discussão
    path('discussions/<int:discussion_id>/chat/', chat_list, name='chat-list'),
]
