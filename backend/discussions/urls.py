from django.urls import path
from .views import DiscussionViewSet, ChatMessageViewSet

# Mapeia os métodos HTTP para as ações da ViewSet
# GET/POST para a lista de discussões
discussion_list = DiscussionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# GET/PUT/PATCH/DELETE para uma discussão específica
discussion_detail = DiscussionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# Ação customizada para encerrar uma discussão
discussion_close = DiscussionViewSet.as_view({
    'post': 'close_discussion'
})

# Ação customizada para reabrir uma discussão
discussion_reopen = DiscussionViewSet.as_view({
    'post': 'reopen_discussion'
})


# GET/POST para a lista de mensagens de um chat
chat_list = ChatMessageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# Lista de todos os endpoints da aplicação 'discussions'
urlpatterns = [
    # Rotas para criar e listar discussões de um projeto
    path('projects/<int:project_id>/discussions/', discussion_list, name='discussion-list'),
    
    # Rotas para ver, editar e excluir uma discussão específica
    path('projects/<int:project_id>/discussions/<int:pk>/', discussion_detail, name='discussion-detail'),

    # Rotas para as ações customizadas
    path('projects/<int:project_id>/discussions/<int:pk>/close/', discussion_close, name='discussion-close'),
    path('projects/<int:project_id>/discussions/<int:pk>/reopen/', discussion_reopen, name='discussion-reopen'),

    # Rota para o chat de uma discussão
    path('discussions/<int:discussion_id>/chat/', chat_list, name='chat-list'),
]