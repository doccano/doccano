from typing import List

from django.shortcuts import get_object_or_404

from examples.assignment.strategies import StrategyName, create_assignment_strategy
from examples.models import Assignment, Example
from projects.models import Member, Project


def bulk_assign(project_id: int, strategy_name: StrategyName, member_ids: List[int], weights: List[int]) -> None:
    project = get_object_or_404(Project, pk=project_id)
    members = Member.objects.filter(project=project, pk__in=member_ids)
    if len(members) != len(member_ids):
        raise ValueError("Invalid member ids")
    # Sort members by member_ids
    members = sorted(members, key=lambda m: member_ids.index(m.id))
    index_to_user = {i: member.user for i, member in enumerate(members)}

    unassigned_examples = Example.objects.filter(project=project, assignments__isnull=True)
    index_to_example = {i: example for i, example in enumerate(unassigned_examples)}
    dataset_size = unassigned_examples.count()

    strategy = create_assignment_strategy(strategy_name, dataset_size, weights)
    assignments = strategy.assign()
    assignments = [
        Assignment(
            project=project,
            example=index_to_example[assignment.example],
            assignee=index_to_user[assignment.user],
        )
        for assignment in assignments
    ]
    Assignment.objects.bulk_create(assignments)
