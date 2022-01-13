from functools import partial

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from members.permissions import IsInProjectOrAdmin

from ...models import Project
from ...permissions import CanEditAnnotation


class BaseListAPI(generics.ListCreateAPIView):
    annotation_class = None
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectOrAdmin]
    swagger_schema = None

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs['project_id'])

    def get_queryset(self):
        queryset = self.annotation_class.objects.filter(example=self.kwargs['example_id'])
        if not self.project.collaborative_annotation:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data['example'] = self.kwargs['example_id']
        try:
            response = super().create(request, args, kwargs)
        except ValidationError as err:
            response = Response({'detail': err.messages}, status=status.HTTP_400_BAD_REQUEST)
        return response

    def perform_create(self, serializer):
        serializer.save(example_id=self.kwargs['example_id'], user=self.request.user)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'annotation_id'
    swagger_schema = None

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs['project_id'])

    def get_permissions(self):
        if self.project.collaborative_annotation:
            self.permission_classes = [IsAuthenticated & IsInProjectOrAdmin]
        else:
            self.permission_classes = [
                IsAuthenticated & IsInProjectOrAdmin & partial(CanEditAnnotation, self.queryset)
            ]
        return super().get_permissions()
