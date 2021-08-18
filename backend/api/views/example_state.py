from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import Example, ExampleState, Project, RoleMapping
from ..permissions import IsInProjectOrAdmin
from ..serializers import ExampleStateSerializer


class ExampleStateList(generics.ListCreateAPIView):
    serializer_class = ExampleStateSerializer
    permission_classes = [IsAuthenticated & IsInProjectOrAdmin]

    @property
    def can_confirm_per_user(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return not project.collaborative_annotation

    def get_queryset(self):
        queryset = ExampleState.objects.filter(example=self.kwargs['example_id'])
        if self.can_confirm_per_user:
            queryset = queryset.filter(confirmed_by=self.request.user)
        current_user_role = RoleMapping.objects.get(user=self.request.user, project_id=self.kwargs['project_id']).role
        ids = [q.id for q in queryset if q.confirmed_user_role == current_user_role]
        queryset = queryset.filter(id__in=ids)
        return queryset

    def perform_create(self, serializer):
        queryset = self.get_queryset()
        if queryset.exists():
            queryset.delete()
        else:
            example = get_object_or_404(Example, pk=self.kwargs['example_id'])
            serializer.save(example=example, confirmed_by=self.request.user)
