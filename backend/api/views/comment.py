from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Comment
from ..permissions import IsInProjectOrAdmin, IsOwnComment
from ..serializers import CommentSerializer


class CommentListDoc(generics.ListCreateAPIView):
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectOrAdmin]
    serializer_class = CommentSerializer
    model = Comment

    def get_queryset(self):
        queryset = self.model.objects.filter(
            example__project_id=self.kwargs['project_id'],
            example=self.kwargs['example_id']
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(example_id=self.kwargs['example_id'], user=self.request.user)


class CommentListProject(generics.ListAPIView):
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectOrAdmin]
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('text',)
    model = Comment

    def get_queryset(self):
        queryset = self.model.objects.filter(
            example__project_id=self.kwargs['project_id']
        )
        return queryset

    def delete(self, request, *args, **kwargs):
        delete_ids = request.data['ids']
        self.model.objects.filter(user=request.user, pk__in=delete_ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    permission_classes = [IsAuthenticated & IsInProjectOrAdmin & IsOwnComment]
