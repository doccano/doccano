import abc
import csv
import io
from collections import defaultdict

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from examples.models import Example, ExampleState
from label_types.models import CategoryType, LabelType, RelationType, SpanType
from labels.models import Category, Label, Relation, Span
from projects.models import Member, Project
from projects.permissions import IsProjectAdmin, IsProjectStaffAndReadOnly
from projects.perspective.models import Question, Answer, QuestionOption


class ProgressAPI(APIView):
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]

    def get(self, request, *args, **kwargs):
        examples = Example.objects.filter(project=self.kwargs["project_id"]).values("id")
        total = examples.count()
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        if project.collaborative_annotation:
            complete = ExampleState.objects.count_done(examples)
        else:
            complete = ExampleState.objects.count_done(examples, user=self.request.user)
        data = {"total": total, "remaining": total - complete, "complete": complete}
        return Response(data=data, status=status.HTTP_200_OK)


class MemberProgressAPI(APIView):
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]

    def get(self, request, *args, **kwargs):
        examples = Example.objects.filter(project=self.kwargs["project_id"]).values("id")
        members = Member.objects.filter(project=self.kwargs["project_id"])
        data = ExampleState.objects.measure_member_progress(examples, members)
        return Response(data=data, status=status.HTTP_200_OK)


class LabelDistribution(abc.ABC, APIView):
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]
    model = Label
    label_type = LabelType

    def get(self, request, *args, **kwargs):
        labels = self.label_type.objects.filter(project=self.kwargs["project_id"])
        examples = Example.objects.filter(project=self.kwargs["project_id"]).values("id")
        members = Member.objects.filter(project=self.kwargs["project_id"])
        data = self.model.objects.calc_label_distribution(examples, members, labels)
        return Response(data=data, status=status.HTTP_200_OK)


class CategoryTypeDistribution(LabelDistribution):
    model = Category
    label_type = CategoryType


class SpanTypeDistribution(LabelDistribution):
    model = Span
    label_type = SpanType


class RelationTypeDistribution(LabelDistribution):
    model = Relation
    label_type = RelationType


class DiscrepancyStatsAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs["project_id"]
        project = get_object_or_404(Project, pk=project_id)

        # Get filter parameters
        label_filter = request.GET.get('label')

        # Get active members only
        active_members = Member.objects.filter(project=project_id).select_related('user')
        active_user_ids = set(member.user_id for member in active_members)

        # Get all examples with annotations
        examples = Example.objects.filter(project=project_id)

        total_discrepancies = 0
        total_agreements = 0
        total_examples_analyzed = 0

        for example in examples:
            # Get users assigned to this specific example
            assigned_user_ids = set(
                example.assignments.filter(assignee_id__in=active_user_ids).values_list('assignee_id', flat=True)
            )

            # Skip examples with less than 2 assigned users
            if len(assigned_user_ids) < 2:
                continue

            # Get all annotations for this example
            annotations_by_user = defaultdict(list)

            # Get spans (only from users assigned to this example)
            spans = Span.objects.filter(example=example).select_related('label', 'user')
            for span in spans:
                # Skip if user is not assigned to this specific example
                if span.user_id not in assigned_user_ids:
                    continue

                label_text = span.label.text if span.label else 'No Label'
                # Apply label filter if specified
                if not label_filter or label_text == label_filter:
                    annotations_by_user[span.user_id].append({
                        'type': 'span',
                        'label': label_text,
                        'start': span.start_offset,
                        'end': span.end_offset
                    })

            # Get categories (only from users assigned to this example)
            categories = Category.objects.filter(example=example).select_related('label', 'user')
            for category in categories:
                # Skip if user is not assigned to this specific example
                if category.user_id not in assigned_user_ids:
                    continue

                label_text = category.label.text if category.label else 'No Label'
                # Apply label filter if specified
                if not label_filter or label_text == label_filter:
                    annotations_by_user[category.user_id].append({
                        'type': 'category',
                        'label': label_text
                    })

            # Only analyze examples that have annotations from multiple users
            user_ids = list(annotations_by_user.keys())
            if len(user_ids) >= 2:
                total_examples_analyzed += 1

                # Check for discrepancies between all pairs of users
                has_discrepancy = False

                # Compare annotations between users
                for i in range(len(user_ids)):
                    for j in range(i + 1, len(user_ids)):
                        user1_annotations = annotations_by_user[user_ids[i]]
                        user2_annotations = annotations_by_user[user_ids[j]]

                        # Compare the sets of annotations
                        if self._annotations_differ(user1_annotations, user2_annotations):
                            has_discrepancy = True
                            break
                    if has_discrepancy:
                        break

                if has_discrepancy:
                    total_discrepancies += 1
                else:
                    total_agreements += 1

        # Calculate percentages
        discrepancy_percentage = (total_discrepancies / total_examples_analyzed * 100) if total_examples_analyzed > 0 else 0
        agreement_percentage = (total_agreements / total_examples_analyzed * 100) if total_examples_analyzed > 0 else 0

        # Calculate user agreements for pairs that actually annotated the same texts
        user_agreements = self._calculate_user_agreements(project_id, label_filter)

        # Get top discrepant examples with real data
        top_discrepant_examples = self._get_top_discrepant_examples(project_id, label_filter)

        # Get label-specific discrepancies
        label_discrepancies = self._calculate_label_discrepancies(project_id, label_filter)

        return Response({
            'total_examples': total_examples_analyzed,
            'total_discrepancies': total_discrepancies,
            'total_agreements': total_agreements,
            'discrepancy_percentage': round(discrepancy_percentage, 2),
            'agreement_percentage': round(agreement_percentage, 2),
            'user_agreements': user_agreements,
            'top_discrepant_examples': top_discrepant_examples,
            'label_discrepancies': label_discrepancies,
            'available_labels': self._get_available_labels(project_id),
            'filter_applied': label_filter
        })

    def _annotations_differ(self, annotations1, annotations2):
        """Compare two sets of annotations to detect discrepancies"""
        # Convert annotations to comparable format
        set1 = set()
        set2 = set()

        for ann in annotations1:
            if ann['type'] == 'span':
                set1.add((ann['label'], ann['start'], ann['end']))
            else:
                set1.add((ann['label'],))

        for ann in annotations2:
            if ann['type'] == 'span':
                set2.add((ann['label'], ann['start'], ann['end']))
            else:
                set2.add((ann['label'],))

        return set1 != set2

    def _get_available_labels(self, project_id):
        labels = set()

        # Get span labels
        span_labels = SpanType.objects.filter(project=project_id).values_list('text', flat=True)
        labels.update(span_labels)

        # Get category labels
        category_labels = CategoryType.objects.filter(project=project_id).values_list('text', flat=True)
        labels.update(category_labels)

        return sorted(list(labels))

    def _calculate_user_agreements(self, project_id, label_filter=None):
        """Calculate agreement rates between pairs of users who actually annotated the same texts"""
        # Get active members only
        active_members = Member.objects.filter(project=project_id).select_related('user')
        active_user_ids = set(member.user_id for member in active_members)

        # Create a mapping of user_id to username
        user_mapping = {member.user_id: member.user.username for member in active_members}

        # Get all examples with annotations
        examples = Example.objects.filter(project=project_id)

        # Track agreements and disagreements between user pairs
        user_pair_stats = defaultdict(lambda: {'agreements': 0, 'disagreements': 0, 'total_comparisons': 0})

        for example in examples:
            # Get users assigned to this specific example
            assigned_user_ids = set(
                example.assignments.filter(assignee_id__in=active_user_ids).values_list('assignee_id', flat=True)
            )

            # Skip examples with less than 2 assigned users
            if len(assigned_user_ids) < 2:
                continue

            # Get all annotations for this example
            annotations_by_user = defaultdict(list)

            # Get spans (only from users assigned to this example)
            spans = Span.objects.filter(example=example).select_related('label', 'user')
            for span in spans:
                # Skip if user is not assigned to this specific example
                if span.user_id not in assigned_user_ids:
                    continue

                label_text = span.label.text if span.label else 'No Label'
                # Apply label filter if specified
                if not label_filter or label_text == label_filter:
                    annotations_by_user[span.user_id].append({
                        'type': 'span',
                        'label': label_text,
                        'start': span.start_offset,
                        'end': span.end_offset
                    })

            # Get categories (only from users assigned to this example)
            categories = Category.objects.filter(example=example).select_related('label', 'user')
            for category in categories:
                # Skip if user is not assigned to this specific example
                if category.user_id not in assigned_user_ids:
                    continue

                label_text = category.label.text if category.label else 'No Label'
                # Apply label filter if specified
                if not label_filter or label_text == label_filter:
                    annotations_by_user[category.user_id].append({
                        'type': 'category',
                        'label': label_text
                    })

            # Only analyze examples that have annotations from multiple users
            user_ids = list(annotations_by_user.keys())
            if len(user_ids) >= 2:
                # Compare annotations between all pairs of users
                for i in range(len(user_ids)):
                    for j in range(i + 1, len(user_ids)):
                        user1_id = user_ids[i]
                        user2_id = user_ids[j]
                        user1_annotations = annotations_by_user[user1_id]
                        user2_annotations = annotations_by_user[user2_id]

                        # Create a consistent pair key (smaller id first)
                        pair_key = (min(user1_id, user2_id), max(user1_id, user2_id))

                        # Compare the sets of annotations
                        if self._annotations_differ(user1_annotations, user2_annotations):
                            user_pair_stats[pair_key]['disagreements'] += 1
                        else:
                            user_pair_stats[pair_key]['agreements'] += 1

                        user_pair_stats[pair_key]['total_comparisons'] += 1

        # Convert to list format with agreement percentages
        user_agreements = []
        for (user1_id, user2_id), stats in user_pair_stats.items():
            if stats['total_comparisons'] > 0:
                agreement_rate = round((stats['agreements'] / stats['total_comparisons']) * 100, 2)
                user1_name = user_mapping.get(user1_id, f'User {user1_id}')
                user2_name = user_mapping.get(user2_id, f'User {user2_id}')

                user_agreements.append({
                    'user_pair': f'{user1_name} vs {user2_name}',
                    'agreement_rate': agreement_rate,
                    'agreements': stats['agreements'],
                    'disagreements': stats['disagreements'],
                    'total_comparisons': stats['total_comparisons']
                })

        # Sort by agreement rate (descending)
        user_agreements.sort(key=lambda x: x['agreement_rate'], reverse=True)

        return user_agreements

    def _get_top_discrepant_examples(self, project_id, label_filter=None, limit=10):
        """Get examples with the highest discrepancy rates"""
        # Get active members only
        active_members = Member.objects.filter(project=project_id).select_related('user')
        active_user_ids = set(member.user_id for member in active_members)

        # Create a mapping of user_id to username
        user_mapping = {member.user_id: member.user.username for member in active_members}

        # Get all examples with annotations
        examples = Example.objects.filter(project=project_id)

        discrepant_examples = []

        for example in examples:
            # Get users assigned to this specific example
            assigned_user_ids = set(
                example.assignments.filter(assignee_id__in=active_user_ids).values_list('assignee_id', flat=True)
            )

            # Skip examples with less than 2 assigned users
            if len(assigned_user_ids) < 2:
                continue

            # Get all annotations for this example
            annotations_by_user = defaultdict(list)

            # Get spans (only from users assigned to this example)
            spans = Span.objects.filter(example=example).select_related('label', 'user')
            for span in spans:
                # Skip if user is not assigned to this specific example
                if span.user_id not in assigned_user_ids:
                    continue

                label_text = span.label.text if span.label else 'No Label'
                # Apply label filter if specified
                if not label_filter or label_text == label_filter:
                    annotations_by_user[span.user_id].append({
                        'type': 'span',
                        'label': label_text,
                        'start': span.start_offset,
                        'end': span.end_offset
                    })

            # Get categories (only from users assigned to this example)
            categories = Category.objects.filter(example=example).select_related('label', 'user')
            for category in categories:
                # Skip if user is not assigned to this specific example
                if category.user_id not in assigned_user_ids:
                    continue

                label_text = category.label.text if category.label else 'No Label'
                # Apply label filter if specified
                if not label_filter or label_text == label_filter:
                    annotations_by_user[category.user_id].append({
                        'type': 'category',
                        'label': label_text
                    })

            # Only analyze examples that have annotations from multiple users
            user_ids = list(annotations_by_user.keys())
            if len(user_ids) >= 2:
                # Count disagreements and agreements for this example
                total_comparisons = 0
                disagreements = 0
                conflicting_labels = set()
                annotator_names = []

                # Compare annotations between all pairs of users
                for i in range(len(user_ids)):
                    for j in range(i + 1, len(user_ids)):
                        user1_id = user_ids[i]
                        user2_id = user_ids[j]
                        user1_annotations = annotations_by_user[user1_id]
                        user2_annotations = annotations_by_user[user2_id]

                        total_comparisons += 1

                        # Compare the sets of annotations
                        if self._annotations_differ(user1_annotations, user2_annotations):
                            disagreements += 1

                            # Collect conflicting labels
                            for ann in user1_annotations + user2_annotations:
                                conflicting_labels.add(ann['label'])

                # Collect annotator names
                for user_id in user_ids:
                    annotator_names.append(user_mapping.get(user_id, f'User {user_id}'))

                # Calculate discrepancy rate for this example
                if total_comparisons > 0:
                    discrepancy_rate = round((disagreements / total_comparisons) * 100, 2)

                    # Only include examples with discrepancies
                    if disagreements > 0:
                        discrepant_examples.append({
                            'id': example.id,
                            'text': example.text,
                            'discrepancy_rate': discrepancy_rate,
                            'conflicting_labels': list(conflicting_labels),
                            'annotator_count': len(user_ids),
                            'annotators': annotator_names,
                            'disagreements': disagreements,
                            'total_comparisons': total_comparisons
                        })

        # Sort by discrepancy rate (descending) and limit results
        discrepant_examples.sort(key=lambda x: x['discrepancy_rate'], reverse=True)

        return discrepant_examples[:limit]

    def _calculate_label_discrepancies(self, project_id, label_filter=None):
        """Calculate discrepancy rates for each label"""
        # Get active members only
        active_members = Member.objects.filter(project=project_id).select_related('user')
        active_user_ids = set(member.user_id for member in active_members)

        # Get all examples with annotations
        examples = Example.objects.filter(project=project_id)

        # Track label statistics
        label_stats = defaultdict(lambda: {'total_examples': 0, 'discrepant_examples': 0})

        for example in examples:
            # Get users assigned to this specific example
            assigned_user_ids = set(
                example.assignments.filter(assignee_id__in=active_user_ids).values_list('assignee_id', flat=True)
            )

            # Skip examples with less than 2 assigned users
            if len(assigned_user_ids) < 2:
                continue

            # Get all annotations for this example
            annotations_by_user = defaultdict(list)

            # Get spans (only from users assigned to this example)
            spans = Span.objects.filter(example=example).select_related('label', 'user')
            for span in spans:
                # Skip if user is not assigned to this specific example
                if span.user_id not in assigned_user_ids:
                    continue

                label_text = span.label.text if span.label else 'No Label'
                # Apply label filter if specified
                if not label_filter or label_text == label_filter:
                    annotations_by_user[span.user_id].append({
                        'type': 'span',
                        'label': label_text,
                        'start': span.start_offset,
                        'end': span.end_offset
                    })

            # Get categories (only from users assigned to this example)
            categories = Category.objects.filter(example=example).select_related('label', 'user')
            for category in categories:
                # Skip if user is not assigned to this specific example
                if category.user_id not in assigned_user_ids:
                    continue

                label_text = category.label.text if category.label else 'No Label'
                # Apply label filter if specified
                if not label_filter or label_text == label_filter:
                    annotations_by_user[category.user_id].append({
                        'type': 'category',
                        'label': label_text
                    })

            # Only analyze examples that have annotations from multiple users
            user_ids = list(annotations_by_user.keys())
            if len(user_ids) >= 2:
                # Collect all labels used by each user for this example
                user_label_sets = {}
                all_labels_in_example = set()

                for user_id in user_ids:
                    user_labels = set()
                    for annotation in annotations_by_user[user_id]:
                        user_labels.add(annotation['label'])
                        all_labels_in_example.add(annotation['label'])
                    user_label_sets[user_id] = user_labels

                # For each label that appears in this example, check if there's disagreement
                for label in all_labels_in_example:
                    label_stats[label]['total_examples'] += 1

                    # Check if there's disagreement about this specific label
                    # Disagreement occurs when some users include the label and others don't
                    users_with_label = []
                    users_without_label = []

                    for user_id in user_ids:
                        if label in user_label_sets[user_id]:
                            users_with_label.append(user_id)
                        else:
                            users_without_label.append(user_id)

                    # There's a discrepancy for this label if some users have it and others don't
                    if len(users_with_label) > 0 and len(users_without_label) > 0:
                        label_stats[label]['discrepant_examples'] += 1

        # Convert to list format with discrepancy rates
        label_discrepancies = []
        for label, stats in label_stats.items():
            if stats['total_examples'] > 0:
                discrepancy_rate = round((stats['discrepant_examples'] / stats['total_examples']) * 100, 2)

                label_discrepancies.append({
                    'label': label,
                    'count': stats['discrepant_examples'],
                    'rate': discrepancy_rate,
                    'total_examples': stats['total_examples']
                })

        # Sort by discrepancy rate (descending)
        label_discrepancies.sort(key=lambda x: x['rate'], reverse=True)

        return label_discrepancies


class PerspectiveStatsAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs["project_id"]
        project = get_object_or_404(Project, pk=project_id)

        # Get filter parameters
        question_filter = request.GET.get('question_id')

        questions = Question.objects.filter(project=project)
        if question_filter:
            questions = questions.filter(id=question_filter)

        stats = {
            'total_questions': questions.count(),
            'total_answers': Answer.objects.filter(question__project=project).count(),
            'questions': []
        }

        for question in questions:
            answers = Answer.objects.filter(question=question)
            question_stats = {
                'id': question.id,
                'text': question.text,
                'question_type': question.question_type,
                'answer_count': answers.count(),
                'response_rate': 0
            }

            # Calculate response rate
            total_members = Member.objects.filter(project=project).count()
            if total_members > 0:
                question_stats['response_rate'] = round((answers.count() / total_members) * 100, 2)

            # Get answer distribution for closed questions
            if question.question_type == 'closed':
                option_stats = []
                for option in question.options.all():
                    option_answers = answers.filter(selected_option=option).count()
                    option_stats.append({
                        'id': option.id,
                        'text': option.text,
                        'count': option_answers,
                        'percentage': round((option_answers / answers.count()) * 100, 2) if answers.count() > 0 else 0
                    })
                question_stats['options'] = option_stats

            stats['questions'].append(question_stats)

        # Get available questions for filter
        all_questions = Question.objects.filter(project=project).values('id', 'text')
        stats['available_questions'] = list(all_questions)

        return Response(stats)


class LabelStatsAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        try:
            project_id = self.kwargs["project_id"]

            # Simple counts first
            span_count = Span.objects.filter(example__project=project_id).count()
            category_count = Category.objects.filter(example__project=project_id).count()
            total_labels = span_count + category_count

            # Get available labels
            span_labels = list(SpanType.objects.filter(project=project_id).values_list('text', flat=True))
            category_labels = list(CategoryType.objects.filter(project=project_id).values_list('text', flat=True))
            available_labels = sorted(list(set(span_labels + category_labels)))

            # Get available users
            available_users = []
            members = Member.objects.filter(project=project_id).select_related('user')
            active_user_ids = set()

            for member in members:
                available_users.append({
                    'id': member.user_id,
                    'username': member.user.username
                })
                active_user_ids.add(member.user_id)

            # Label distribution with users
            label_distribution = {}

            # Process spans (only from active members)
            spans = Span.objects.filter(example__project=project_id).select_related('label', 'user')
            for span in spans:
                # Skip if user is no longer a member of the project
                if span.user_id not in active_user_ids:
                    continue

                label_text = span.label.text if span.label else 'No Label'

                if label_text not in label_distribution:
                    label_distribution[label_text] = {
                        'label': label_text,
                        'count': 0,
                        'users': set()
                    }

                label_distribution[label_text]['count'] += 1
                label_distribution[label_text]['users'].add(span.user)

            # Process categories (only from active members)
            categories = Category.objects.filter(example__project=project_id).select_related('label', 'user')
            for category in categories:
                # Skip if user is no longer a member of the project
                if category.user_id not in active_user_ids:
                    continue

                label_text = category.label.text if category.label else 'No Label'

                if label_text not in label_distribution:
                    label_distribution[label_text] = {
                        'label': label_text,
                        'count': 0,
                        'users': set()
                    }

                label_distribution[label_text]['count'] += 1
                label_distribution[label_text]['users'].add(category.user)

            # Recalculate total labels (only from active members)
            total_labels_active = sum(data['count'] for data in label_distribution.values())

            # Convert to list and add percentages
            label_distribution_list = []
            for label_data in label_distribution.values():
                percentage = round((label_data['count'] / total_labels_active * 100), 2) if total_labels_active > 0 else 0
                # Only include users that are still active members
                users_list = [
                    {'id': user.id, 'username': user.username}
                    for user in label_data['users']
                    if user.id in active_user_ids
                ]

                label_distribution_list.append({
                    'label': label_data['label'],
                    'count': label_data['count'],
                    'percentage': percentage,
                    'users': users_list
                })

            # Sort by count
            label_distribution_list.sort(key=lambda x: x['count'], reverse=True)

            # Basic user performance
            user_performance = []
            for member in members:
                user_span_count = Span.objects.filter(example__project=project_id, user=member.user).count()
                user_category_count = Category.objects.filter(example__project=project_id, user=member.user).count()
                user_total = user_span_count + user_category_count

                user_examples = set()
                user_examples.update(Span.objects.filter(example__project=project_id, user=member.user).values_list('example_id', flat=True))
                user_examples.update(Category.objects.filter(example__project=project_id, user=member.user).values_list('example_id', flat=True))

                examples_count = len(user_examples)
                labels_per_example = round(user_total / examples_count, 2) if examples_count > 0 else 0

                user_performance.append({
                    'user_id': member.user_id,
                    'username': member.user.username,
                    'total_labels': user_total,
                    'examples_labeled': examples_count,
                    'labels_per_example': labels_per_example
                })

            # Sort by total labels
            user_performance.sort(key=lambda x: x['total_labels'], reverse=True)

            # Calculate total examples
            span_examples = set(Span.objects.filter(example__project=project_id).values_list('example_id', flat=True))
            category_examples = set(Category.objects.filter(example__project=project_id).values_list('example_id', flat=True))
            total_examples = len(span_examples.union(category_examples))

            avg_labels_per_example = round(total_labels / total_examples, 2) if total_examples > 0 else 0

            return Response({
                'total_labels': total_labels_active,  # Use active members count
                'total_examples': total_examples,
                'total_users': len(available_users),
                'avg_labels_per_example': round(total_labels_active / total_examples, 2) if total_examples > 0 else 0,
                'label_distribution': label_distribution_list,
                'user_performance': user_performance,
                'available_labels': available_labels,
                'available_users': available_users
            })

        except Exception as e:
            print(f"Error in LabelStatsAPI: {e}")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExportReportsAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs["project_id"]
        export_type = request.GET.get('type', 'labels')  # 'discrepancies', 'perspectives', or 'labels'
        format_type = request.GET.get('format', 'csv')  # 'csv' or 'pdf'

        if export_type == 'discrepancies':
            return self._export_discrepancies(project_id, format_type)
        elif export_type == 'perspectives':
            return self._export_perspectives(project_id, format_type)
        elif export_type == 'labels':
            return self._export_labels(project_id, format_type, request)
        else:
            return Response({'error': 'Invalid export type'}, status=status.HTTP_400_BAD_REQUEST)

    def _export_discrepancies(self, project_id, format_type):
        if format_type != 'csv':
            return Response({'error': 'Only CSV format supported for now'}, status=status.HTTP_400_BAD_REQUEST)

        # Get active members only
        active_members = Member.objects.filter(project=project_id).select_related('user')
        active_user_ids = set(member.user_id for member in active_members)

        # Get discrepancy data
        examples = Example.objects.filter(project=project_id)

        # Create CSV
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(['Example ID', 'Text', 'Has Discrepancy', 'Agreement %', 'Annotators', 'Labels', 'Annotation Details'])

        for example in examples:
            # Get users assigned to this specific example
            assigned_user_ids = set(
                example.assignments.filter(assignee_id__in=active_user_ids).values_list('assignee_id', flat=True)
            )

            # Skip examples with less than 2 assigned users
            if len(assigned_user_ids) < 2:
                continue

            # Get annotations for this example
            annotations_by_user = defaultdict(list)

            # Get spans (only from users assigned to this example)
            spans = Span.objects.filter(example=example).select_related('label', 'user')
            for span in spans:
                # Skip if user is not assigned to this specific example
                if span.user_id not in assigned_user_ids:
                    continue

                label_text = span.label.text if span.label else 'No Label'
                annotations_by_user[span.user_id].append({
                    'type': 'span',
                    'label': label_text,
                    'start': span.start_offset,
                    'end': span.end_offset
                })

            # Get categories (only from users assigned to this example)
            categories = Category.objects.filter(example=example).select_related('label', 'user')
            for category in categories:
                # Skip if user is not assigned to this specific example
                if category.user_id not in assigned_user_ids:
                    continue

                label_text = category.label.text if category.label else 'No Label'
                annotations_by_user[category.user_id].append({
                    'type': 'category',
                    'label': label_text
                })

            # Only include examples with multiple annotators
            user_ids = list(annotations_by_user.keys())
            if len(user_ids) < 2:
                continue

            # Check for discrepancies
            has_discrepancy = False
            for i in range(len(user_ids)):
                for j in range(i + 1, len(user_ids)):
                    user1_annotations = annotations_by_user[user_ids[i]]
                    user2_annotations = annotations_by_user[user_ids[j]]

                    if self._annotations_differ(user1_annotations, user2_annotations):
                        has_discrepancy = True
                        break
                if has_discrepancy:
                    break

            # Calculate agreement percentage
            agreement_percentage = 0 if has_discrepancy else 100

            # Get member names
            member_names = []
            for user_id in user_ids:
                try:
                    member = Member.objects.get(project=project_id, user_id=user_id)
                    member_names.append(member.username)
                except Member.DoesNotExist:
                    member_names.append(f'User {user_id}')

            # Get all unique labels
            all_labels = set()
            annotation_details = []
            for user_id, user_annotations in annotations_by_user.items():
                user_labels = []
                for ann in user_annotations:
                    all_labels.add(ann['label'])
                    if ann['type'] == 'span':
                        user_labels.append(f"{ann['label']}({ann['start']}-{ann['end']})")
                    else:
                        user_labels.append(ann['label'])

                try:
                    member = Member.objects.get(project=project_id, user_id=user_id)
                    username = member.username
                except Member.DoesNotExist:
                    username = f'User {user_id}'

                annotation_details.append(f"{username}: {', '.join(user_labels)}")

            writer.writerow([
                example.id,
                example.text[:100] + '...' if len(example.text) > 100 else example.text,
                'Yes' if has_discrepancy else 'No',
                f'{agreement_percentage}%',
                ', '.join(member_names),
                ', '.join(sorted(all_labels)),
                ' | '.join(annotation_details)
            ])

        # Create response
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="discrepancies_report_{project_id}.csv"'
        return response

    def _export_perspectives(self, project_id, format_type):
        if format_type != 'csv':
            return Response({'error': 'Only CSV format supported for now'}, status=status.HTTP_400_BAD_REQUEST)

        # Get perspective data
        questions = Question.objects.filter(project=project_id)

        # Create CSV
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(['Question ID', 'Question Text', 'Question Type', 'Total Answers', 'Response Rate'])

        total_members = Member.objects.filter(project=project_id).count()

        for question in questions:
            answers_count = Answer.objects.filter(question=question).count()
            response_rate = round((answers_count / total_members) * 100, 2) if total_members > 0 else 0

            writer.writerow([
                question.id,
                question.text,
                question.question_type,
                answers_count,
                f'{response_rate}%'
            ])

        # Create response
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="perspectives_report_{project_id}.csv"'
        return response

    def _export_labels(self, project_id, format_type, request):
        if format_type != 'csv':
            return Response({'error': 'Only CSV format supported for now'}, status=status.HTTP_400_BAD_REQUEST)

        # Get filter parameters
        label_filter = request.GET.get('label')
        user_filter = request.GET.get('user_id')

        # Get label data
        all_spans = Span.objects.filter(example__project=project_id).select_related('label', 'user', 'example')
        all_categories = Category.objects.filter(example__project=project_id).select_related('label', 'user', 'example')

        # Apply filters
        if label_filter:
            all_spans = all_spans.filter(label__text=label_filter)
            all_categories = all_categories.filter(label__text=label_filter)

        if user_filter:
            all_spans = all_spans.filter(user_id=user_filter)
            all_categories = all_categories.filter(user_id=user_filter)

        # Create CSV
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(['Example ID', 'Text', 'Label', 'Label Type', 'User', 'Start Offset', 'End Offset', 'Created At'])

        # Write spans
        for span in all_spans:
            writer.writerow([
                span.example.id,
                span.example.text[:100] + '...' if len(span.example.text) > 100 else span.example.text,
                span.label.text if span.label else 'No Label',
                'Span',
                span.user.username,
                span.start_offset,
                span.end_offset,
                span.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(span, 'created_at') else ''
            ])

        # Write categories
        for category in all_categories:
            writer.writerow([
                category.example.id,
                category.example.text[:100] + '...' if len(category.example.text) > 100 else category.example.text,
                category.label.text if category.label else 'No Label',
                'Category',
                category.user.username,
                '',  # No start offset for categories
                '',  # No end offset for categories
                category.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(category, 'created_at') else ''
            ])

        # Create response
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="label_analysis_{project_id}.csv"'
        return response
