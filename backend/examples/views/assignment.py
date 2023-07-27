from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from examples.models import Assignment
from examples.serializers import AssignmentSerializer
from projects.models import Project
from projects.permissions import IsProjectAdmin, IsProjectStaffAndReadOnly


class AssignmentList(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ("created_at", "updated_at")
    model = Assignment

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_id"])

    def get_queryset(self):
        queryset = self.model.objects.filter(project=self.project, assignee=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(project=self.project)


class AssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    lookup_url_kwarg = "assignment_id"
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]


class ResetAssignment(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_id"])

    def delete(self, *args, **kwargs):
        Assignment.objects.filter(project=self.project).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
