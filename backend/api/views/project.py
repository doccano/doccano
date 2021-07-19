from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..exceptions import ProjectCreationPermissionDenied
from ..models import Project
from ..permissions import IsInProjectReadOnlyOrAdmin
from ..serializers import ProjectPolymorphicSerializer, ProjectSerializer


class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectPolymorphicSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return self.request.user.projects

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save(users=[self.request.user])
        else:
            raise ProjectCreationPermissionDenied()

    def delete(self, request, *args, **kwargs):
        delete_ids = request.data['ids']
        projects = Project.objects.filter(
            role_mappings__user=self.request.user,
            role_mappings__role__name=settings.ROLE_PROJECT_ADMIN,
            pk__in=delete_ids
        )
        # Todo: I want to use bulk delete.
        # But it causes the constraint error.
        # See https://github.com/django-polymorphic/django-polymorphic/issues/229
        for project in projects:
            project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_url_kwarg = 'project_id'
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]
