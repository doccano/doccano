from django.shortcuts import get_object_or_404

from examples.assignment.strategies import StrategyName, create_assignment_strategy
from examples.assignment.workload import WorkloadAllocation
from examples.models import Assignment, Example
from projects.models import Member, Project


def bulk_assign(project_id: int, workload_allocation: WorkloadAllocation, strategy_name: StrategyName) -> None:
    project = get_object_or_404(Project, pk=project_id)
    members = Member.objects.filter(project=project, pk__in=workload_allocation.member_ids)
    if len(members) != len(workload_allocation.member_ids):
        raise ValueError("Invalid member ids")
    # Sort members by workload_allocation.member_ids
    members = sorted(members, key=lambda m: workload_allocation.member_ids.index(m.id))

    unassigned_examples = Example.objects.filter(project=project, assignments__isnull=True)
    dataset_size = unassigned_examples.count()

    strategy = create_assignment_strategy(strategy_name, dataset_size, workload_allocation.weights)
    assignments = strategy.assign()
    assignments = [
        Assignment(
            project=project,
            example=unassigned_examples[assignment.example],
            assignee=members[assignment.user].user,
        )
        for assignment in assignments
    ]
    Assignment.objects.bulk_create(assignments)
