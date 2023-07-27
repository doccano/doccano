from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from pydantic import ValidationError
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from examples.assignment.strategies import StrategyName, create_assignment_strategy
from examples.assignment.workload import WorkloadAllocation
from examples.models import Assignment
from examples.serializers import AssignmentSerializer
from projects.models import Member, Project
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


class BulkAssignment(APIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, *args, **kwargs):
        try:
            strategy_name = StrategyName[self.request.data["strategy_name"]]
        except KeyError:
            return Response(
                {"detail": "Invalid strategy name"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            workload_allocation = WorkloadAllocation(workloads=self.request.data["workloads"])
        except ValidationError as e:
            return Response(
                {"detail": e.errors()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        members = Member.objects.filter(project=project, pk__in=workload_allocation.member_ids)
        if len(members) != len(workload_allocation.member_ids):
            return Response(
                {"detail": "Invalid member ids"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Sort members by workload_allocation.member_ids
        members = sorted(members, key=lambda m: workload_allocation.member_ids.index(m.id))

        dataset_size = project.examples.count()  # Todo: unassigned examples
        strategy = create_assignment_strategy(strategy_name, dataset_size, workload_allocation.weights)
        assignments = strategy.assign()
        example_ids = project.examples.values_list("pk", flat=True)
        assignments = [
            Assignment(
                project=project,
                example=example_ids[assignment.example],
                assignee=members[assignment.user].user,
            )
            for assignment in assignments
        ]
        Assignment.objects.bulk_create(assignments)
        return Response(status=status.HTTP_201_CREATED)
