from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from projects.models import Tag
from projects.permissions import IsProjectAdmin, IsProjectStaffAndReadOnly
from projects.serializers import TagSerializer


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]

    def get_queryset(self):
        return Tag.objects.filter(project=self.kwargs["project_id"])

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs["project_id"])


class TagDetail(generics.DestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_url_kwarg = "tag_id"
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]
