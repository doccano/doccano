from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..exceptions import RoleAlreadyAssignedException, RoleConstraintException
from ..models import Project, Role, RoleMapping
from ..permissions import IsProjectAdmin
from ..serializers import RoleMappingSerializer, RoleSerializer


class Roles(generics.ListAPIView):
    serializer_class = RoleSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()


class RoleMappingList(generics.ListCreateAPIView):
    serializer_class = RoleMappingSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs['project_id'])

    def get_queryset(self):
        return self.project.role_mappings

    def perform_create(self, serializer):
        try:
            serializer.save(project=self.project)
        except IntegrityError:
            raise RoleAlreadyAssignedException

    def delete(self, request, *args, **kwargs):
        delete_ids = request.data['ids']
        RoleMapping.objects.filter(project=self.project, pk__in=delete_ids)\
            .exclude(user=self.request.user)\
            .delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoleMappingDetail(generics.RetrieveUpdateAPIView):
    queryset = RoleMapping.objects.all()
    serializer_class = RoleMappingSerializer
    lookup_url_kwarg = 'rolemapping_id'
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def perform_update(self, serializer):
        project_id = self.kwargs['project_id']
        id = self.kwargs['rolemapping_id']
        role = serializer.validated_data['role']
        if not RoleMapping.objects.can_update(project_id, id, role.name):
            raise RoleConstraintException
        try:
            super().perform_update(serializer)
        except IntegrityError:
            raise RoleAlreadyAssignedException
