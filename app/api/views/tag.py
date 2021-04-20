from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from ..models import Project, Tag
from ..serializers import TagSerializer


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    pagination_class = None

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return project.tags

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        serializer.save(project=project)

    def delete(self, request, *args, **kwargs):
        delete_id = request.data['id']
        Tag.objects.get(id=delete_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
