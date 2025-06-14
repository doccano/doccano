from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from examples.models import Comment
from examples.permissions import IsOwnComment
from examples.serializers import CommentSerializer
from projects.permissions import IsProjectMember


class CommentList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & IsProjectMember]
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ["example"]
    search_fields = ("text",)
    ordering_fields = ("created_at", "example")

    def get_queryset(self):
        queryset = Comment.objects.filter(example__project_id=self.kwargs["project_id"])
        return queryset

    def perform_create(self, serializer):
        serializer.save(example_id=self.request.query_params.get("example"), user=self.request.user)

    def delete(self, request, *args, **kwargs):
        delete_ids = request.data["ids"]
        Comment.objects.filter(user=request.user, pk__in=delete_ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = "comment_id"
    permission_classes = [IsAuthenticated & IsProjectMember & IsOwnComment]
