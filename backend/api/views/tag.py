from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import Project, Tag
from ..permissions import IsInProjectReadOnlyOrAdmin
from ..serializers import TagSerializer


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return project.tags

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        serializer.save(project=project)


class TagDetail(generics.DestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_url_kwarg = 'tag_id'
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]
