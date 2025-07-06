import abc
import csv
import io
from collections import defaultdict

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
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
        text_filter = request.GET.get('text')

        # Get active members only
        active_members = Member.objects.filter(project=project_id).select_related('user')
        active_user_ids = set(member.user_id for member in active_members)

        # Get all examples with annotations, apply text filter if provided
        examples = Example.objects.filter(project=project_id)
        if text_filter:
            examples = examples.filter(text__icontains=text_filter)

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

        # Calculate severity distribution
        severity_distribution = self._calculate_severity_distribution(total_examples_analyzed, total_discrepancies, discrepancy_percentage)

        return Response({
            'total_examples': total_examples_analyzed,
            'total_discrepancies': total_discrepancies,
            'total_agreements': total_agreements,
            'discrepancy_percentage': round(discrepancy_percentage, 2),
            'agreement_percentage': round(agreement_percentage, 2),
            'user_agreements': user_agreements,
            'top_discrepant_examples': top_discrepant_examples,
            'label_discrepancies': label_discrepancies,
            'severity_distribution': severity_distribution,
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

    def _calculate_severity_distribution(self, total_examples, total_discrepancies, discrepancy_percentage):
        """Calculate severity distribution based on discrepancy rates"""
        if total_examples == 0 or total_discrepancies == 0:
            return []

        # For small numbers of discrepancies, assign all to a single severity level
        # based on the overall discrepancy percentage
        severity_level = None

        if discrepancy_percentage >= 75:
            severity_level = 'critical'
        elif discrepancy_percentage >= 50:
            severity_level = 'high'
        elif discrepancy_percentage >= 25:
            severity_level = 'medium'
        else:
            severity_level = 'low'

        # Return all discrepancies as a single severity level
        return [{
            'level': severity_level,
            'count': total_discrepancies,
            'percentage': 100.0
        }]


class PerspectiveStatsAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        try:
            project_id = self.kwargs["project_id"]

            # Simplified version to test basic functionality
            stats = {
                'total_questions': 0,
                'total_answers': 0,
                'questions': [],
                'available_questions': []
            }

            # Try to get project first
            try:
                project = get_object_or_404(Project, pk=project_id)
            except Exception as e:
                print(f"Error getting project {project_id}: {e}")
                return Response(stats)

            # Try to get questions
            try:
                questions = Question.objects.filter(project=project)
                stats['total_questions'] = questions.count()

                # Get filter parameters
                question_filter = request.GET.get('question_id')
                text_filter = request.GET.get('text')
                
                if question_filter:
                    questions = questions.filter(id=question_filter)
                if text_filter:
                    questions = questions.filter(text__icontains=text_filter)

                # Get total answers
                stats['total_answers'] = Answer.objects.filter(question__project=project).count()

                # Process each question
                for question in questions:
                    try:
                        answers = Answer.objects.filter(question=question)
                        question_stats = {
                            'id': question.id,
                            'text': question.text,
                            'question_type': question.question_type,
                            'answer_count': answers.count(),
                            'response_rate': 0
                        }

                        # Calculate response rate
                        try:
                            total_members = Member.objects.filter(project=project).count()
                            if total_members > 0:
                                question_stats['response_rate'] = round((answers.count() / total_members) * 100, 2)
                        except Exception as e:
                            print(f"Error calculating response rate: {e}")

                        # Get answer distribution for closed questions
                        if question.question_type == 'closed':
                            try:
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
                            except Exception as e:
                                print(f"Error processing options: {e}")
                                question_stats['options'] = []

                        stats['questions'].append(question_stats)
                    except Exception as e:
                        print(f"Error processing question {question.id}: {e}")
                        continue

                # Get available questions for filter
                try:
                    all_questions = Question.objects.filter(project=project).values('id', 'text')
                    stats['available_questions'] = list(all_questions)
                except Exception as e:
                    print(f"Error getting available questions: {e}")
                    stats['available_questions'] = []

            except Exception as e:
                print(f"Error processing questions: {e}")

            return Response(stats)

        except Exception as e:
            print(f"Error in PerspectiveStatsAPI: {e}")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LabelStatsAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        try:
            project_id = self.kwargs["project_id"]
            
            # Get filter parameters
            label_filter = request.GET.get('label')
            user_filter = request.GET.get('user_id')
            text_filter = request.GET.get('text')

            # Base querysets
            examples_query = Example.objects.filter(project=project_id)
            
            # Apply text filter to examples if provided
            if text_filter:
                examples_query = examples_query.filter(text__icontains=text_filter)
                
            example_ids = list(examples_query.values_list('id', flat=True))

            # Simple counts with filters applied
            spans_query = Span.objects.filter(example__project=project_id)
            categories_query = Category.objects.filter(example__project=project_id)
            
            if example_ids:
                spans_query = spans_query.filter(example_id__in=example_ids)
                categories_query = categories_query.filter(example_id__in=example_ids)
            
            if user_filter:
                spans_query = spans_query.filter(user_id=user_filter)
                categories_query = categories_query.filter(user_id=user_filter)
                
            if label_filter:
                spans_query = spans_query.filter(label__text=label_filter)
                categories_query = categories_query.filter(label__text=label_filter)

            span_count = spans_query.count()
            category_count = categories_query.count()
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

            # Process spans (only from active members, with filters applied)
            for span in spans_query.select_related('label', 'user'):
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

            # Process categories (only from active members, with filters applied)
            for category in categories_query.select_related('label', 'user'):
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

            # Basic user performance with filters applied
            user_performance = []
            for member in members:
                # Apply the same filters to user performance calculations
                user_spans_query = Span.objects.filter(example__project=project_id, user=member.user)
                user_categories_query = Category.objects.filter(example__project=project_id, user=member.user)
                
                if example_ids:
                    user_spans_query = user_spans_query.filter(example_id__in=example_ids)
                    user_categories_query = user_categories_query.filter(example_id__in=example_ids)
                    
                if label_filter:
                    user_spans_query = user_spans_query.filter(label__text=label_filter)
                    user_categories_query = user_categories_query.filter(label__text=label_filter)
                
                user_span_count = user_spans_query.count()
                user_category_count = user_categories_query.count()
                user_total = user_span_count + user_category_count

                # Apply same filters to user examples calculation
                user_examples = set()
                user_examples.update(user_spans_query.values_list('example_id', flat=True))
                user_examples.update(user_categories_query.values_list('example_id', flat=True))

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

            # Calculate total examples with filters applied
            if example_ids:
                total_examples = len(example_ids)
            else:
                span_examples = set(Span.objects.filter(example__project=project_id).values_list('example_id', flat=True))
                category_examples = set(Category.objects.filter(example__project=project_id).values_list('example_id', flat=True))
                total_examples = len(span_examples.union(category_examples))

            return Response({
                'total_labels': total_labels,  # Use filtered count
                'total_examples': total_examples,
                'total_users': len(available_users),
                'avg_labels_per_example': round(total_labels / total_examples, 2) if total_examples > 0 else 0,
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

            # Get spans (only from users assigned to this specific example)
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


class DatasetDetailsAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectStaffAndReadOnly]
    
    def get(self, request, *args, **kwargs):
        try:
            project_id = self.kwargs["project_id"]
            project = get_object_or_404(Project, pk=project_id)
            
            # Get filter parameters
            text_filter = request.GET.get('text')
            user_filter = request.GET.get('user_id')
            label_filter = request.GET.get('label')
            discrepancy_filter = request.GET.get('discrepancy')
            perspective_filter = request.GET.get('question_id')
            
            # Get all examples with their annotations and assignments
            examples_queryset = Example.objects.filter(project=project_id).prefetch_related(
                'assignments__assignee',
                'spans__label',
                'spans__user',
                'categories__label', 
                'categories__user'
            )
            
            # Apply text filter
            if text_filter:
                examples_queryset = examples_queryset.filter(text__icontains=text_filter)
            
            # Apply user filter - only examples that this user annotated
            if user_filter:
                try:
                    user_id = int(user_filter)
                    examples_queryset = examples_queryset.filter(
                        Q(spans__user_id=user_id) | Q(categories__user_id=user_id)
                    ).distinct()
                except (ValueError, TypeError):
                    pass
            
            # Apply label filter
            if label_filter:
                examples_queryset = examples_queryset.filter(
                    Q(spans__label__text__icontains=label_filter) | 
                    Q(categories__label__text__icontains=label_filter)
                ).distinct()
            
            examples = examples_queryset
            
            dataset_details = []
            
            for example in examples:
                # Get assigned users
                assigned_users = []
                for assignment in example.assignments.all():
                    if assignment.assignee:
                        assigned_users.append(assignment.assignee.username)
                
                # Get annotations (spans and categories)
                annotations = []
                
                # Get spans
                for span in example.spans.all():
                    label_text = span.label.text if span.label else 'No Label'
                    user_name = span.user.username if span.user else 'Unknown'
                    annotations.append(f"{label_text} (by {user_name})")
                
                # Get categories
                for category in example.categories.all():
                    label_text = category.label.text if category.label else 'No Label'
                    user_name = category.user.username if category.user else 'Unknown'
                    annotations.append(f"{label_text} (by {user_name})")
                
                # Check for discrepancies
                user_labels = defaultdict(set)
                
                # Collect labels by user for spans
                for span in example.spans.all():
                    if span.user and span.label:
                        user_labels[span.user_id].add(span.label.text)
                
                # Collect labels by user for categories  
                for category in example.categories.all():
                    if category.user and category.label:
                        user_labels[category.user_id].add(category.label.text)
                
                # Determine if there's a discrepancy
                has_discrepancy = "No"
                if len(user_labels) > 1:
                    # Check if different users have different labels
                    all_label_sets = list(user_labels.values())
                    for i, labels1 in enumerate(all_label_sets):
                        for j, labels2 in enumerate(all_label_sets[i+1:], i+1):
                            if labels1 != labels2:
                                has_discrepancy = "Yes"
                                break
                        if has_discrepancy == "Yes":
                            break
                
                # Participation: show assigned vs who actually annotated
                annotating_users = set()
                annotating_user_objects = []
                for span in example.spans.all():
                    if span.user:
                        annotating_users.add(span.user.username)
                        annotating_user_objects.append({'id': span.user.id, 'username': span.user.username})
                for category in example.categories.all():
                    if category.user:
                        annotating_users.add(category.user.username)
                        annotating_user_objects.append({'id': category.user.id, 'username': category.user.username})
                
                # Remove duplicates from annotating_user_objects
                unique_annotating_users = []
                seen_user_ids = set()
                for user_obj in annotating_user_objects:
                    if user_obj['id'] not in seen_user_ids:
                        unique_annotating_users.append(user_obj)
                        seen_user_ids.add(user_obj['id'])
                
                # Calculate participation percentage
                total_assigned = len(assigned_users)
                total_annotating = len(annotating_users)
                participation_percentage = (total_annotating / total_assigned * 100) if total_assigned > 0 else 0
                
                participation_numbers = f"{total_annotating}/{total_assigned}"
                participation_users = ', '.join(assigned_users) if assigned_users else 'No users assigned'
                
                # Build detailed annotation information - Group by label
                annotation_details = {}
                
                # Process spans
                for span in example.spans.all():
                    if span.label:
                        label_text = span.label.text
                        if label_text not in annotation_details:
                            annotation_details[label_text] = {
                                'label': label_text,
                                'users': [],
                                'positions': [],
                                'types': set()
                            }
                        
                        if span.user:
                            # Check if user is already in the list for this label
                            user_exists = any(u['id'] == span.user.id for u in annotation_details[label_text]['users'])
                            if not user_exists:
                                annotation_details[label_text]['users'].append({
                                    'id': span.user.id, 
                                    'username': span.user.username
                                })
                        
                        # Add position if available
                        if hasattr(span, 'start_offset') and hasattr(span, 'end_offset'):
                            annotation_details[label_text]['positions'].append({
                                'start': span.start_offset,
                                'end': span.end_offset
                            })
                        
                        annotation_details[label_text]['types'].add('span')
                
                # Process categories
                for category in example.categories.all():
                    if category.label:
                        label_text = category.label.text
                        if label_text not in annotation_details:
                            annotation_details[label_text] = {
                                'label': label_text,
                                'users': [],
                                'positions': [],
                                'types': set()
                            }
                        
                        if category.user:
                            # Check if user is already in the list for this label
                            user_exists = any(u['id'] == category.user.id for u in annotation_details[label_text]['users'])
                            if not user_exists:
                                annotation_details[label_text]['users'].append({
                                    'id': category.user.id, 
                                    'username': category.user.username
                                })
                        
                        annotation_details[label_text]['types'].add('category')
                
                # Convert to list and clean up types
                annotation_details_list = []
                for label_data in annotation_details.values():
                    label_data['types'] = list(label_data['types'])
                    annotation_details_list.append(label_data)
                
                # Apply discrepancy filter
                should_include = True
                if discrepancy_filter:
                    if discrepancy_filter == 'with' and has_discrepancy == "No":
                        should_include = False
                    elif discrepancy_filter == 'without' and has_discrepancy == "Yes":
                        should_include = False
                
                if should_include:
                    dataset_details.append({
                        'id': example.id,
                        'text': example.text[:50] + '...' if len(example.text) > 50 else example.text,
                        'full_text': example.text,
                        'discrepancy': has_discrepancy,
                        'participationNumbers': participation_numbers,
                        'participationPercentage': participation_percentage,
                        'participationUsers': participation_users,
                        'annotationDetails': annotation_details_list,
                        'assigned_users': assigned_users,
                        'annotating_users': list(annotating_users)
                    })
            
            # Calculate user details
            user_details = []
            all_members = Member.objects.filter(project=project_id).select_related('user')
            for member in all_members:
                user = member.user
                # Get all examples assigned to this user (sem filtro extra)
                assigned_examples = Example.objects.filter(
                    project=project_id,
                    assignments__assignee=user
                ).distinct()
                texts_assigned = assigned_examples.count()
                # Get examples that this user realmente anotou (sem filtro extra)
                labeled_example_ids = set()
                user_spans = Span.objects.filter(
                    example__project=project_id,
                    user=user
                ).values_list('example_id', flat=True)
                labeled_example_ids.update(user_spans)
                user_categories = Category.objects.filter(
                    example__project=project_id,
                    user=user
                ).values_list('example_id', flat=True)
                labeled_example_ids.update(user_categories)
                texts_labeled = len(labeled_example_ids)
                # Total labels usados por esse user
                total_spans = Span.objects.filter(example__project=project_id, user=user).count()
                total_categories = Category.objects.filter(example__project=project_id, user=user).count()
                total_labels = total_spans + total_categories
                participation = (texts_labeled / texts_assigned * 100) if texts_assigned > 0 else 0
                user_details.append({
                    'id': user.id,
                    'username': user.username,
                    'textsAssigned': texts_assigned,
                    'textsLabeled': texts_labeled,
                    'textLabelingPercentage': participation,
                    'totalLabels': total_labels,
                    'participation': participation
                })
            # Calculate perspective details
            perspective_details = []
            try:
                questions_queryset = Question.objects.filter(project=project_id)
                
                # Apply perspective filter - only show specific question
                if perspective_filter:
                    try:
                        question_id = int(perspective_filter)
                        questions_queryset = questions_queryset.filter(id=question_id)
                    except (ValueError, TypeError):
                        pass
                
                questions = questions_queryset
                total_members = all_members.count()
                
                print(f"Found {questions.count()} questions for project {project_id}")
                
                for question in questions:
                    # Get answers for this question
                    answers_queryset = Answer.objects.filter(question=question)
                    
                    # Apply user filter to answers
                    if user_filter:
                        try:
                            user_id = int(user_filter)
                            answers_queryset = answers_queryset.filter(user_id=user_id)
                        except (ValueError, TypeError):
                            pass
                    
                    answer_count = answers_queryset.count()
                    
                    print(f"Question '{question.text}' has {answer_count} answers")
                    
                    # Calculate response rate based on filtered users
                    if user_filter:
                        # When filtering by user, response rate is either 0% or 100%
                        response_rate = 100.0 if answer_count > 0 else 0.0
                    else:
                        # Normal response rate calculation
                        response_rate = (answer_count / total_members * 100) if total_members > 0 else 0
                    
                    # Only include questions that have answers or if no user filter is applied
                    if not user_filter or answer_count > 0:
                        perspective_details.append({
                            'id': question.id,
                            'question': question.text,
                            'type': question.question_type,
                            'answers': answer_count,
                            'responseRate': response_rate
                        })
                
                print(f"Created perspective details: {len(perspective_details)} items")
                
            except Exception as e:
                print(f"Error processing perspective details: {e}")
                import traceback
                traceback.print_exc()
            
            return Response({
                'dataset_details': dataset_details,
                'user_details': user_details,
                'perspective_details': perspective_details,
                'total_examples': len(dataset_details),
                'total_users': len(user_details),
                'total_questions': len(perspective_details)
            })
            
        except Exception as e:
            print(f"Error in DatasetDetailsAPI: {e}")
            import traceback
            traceback.print_exc()
            return Response({
                'error': str(e),
                'dataset_details': [],
                'total_examples': 0
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DatasetTextsAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectStaffAndReadOnly]
    
    def get(self, request, *args, **kwargs):
        try:
            project_id = self.kwargs["project_id"]
            
            # Get unique text samples for dropdown (first 50 chars of each text)
            examples = Example.objects.filter(project=project_id).values_list('text', flat=True)
            
            # Create unique text options for dropdown
            text_options = []
            seen_texts = set()
            
            for text in examples:
                # Use first 50 characters as the option
                text_preview = text[:50] + '...' if len(text) > 50 else text
                if text_preview not in seen_texts:
                    text_options.append({
                        'text': text_preview,
                        'value': text,  # Full text for filtering
                        'preview': text_preview
                    })
                    seen_texts.add(text_preview)
                    
                # Limit to avoid too many options
                if len(text_options) >= 100:
                    break
            
            return Response({
                'text_options': text_options,
                'total_texts': len(text_options)
            })
            
        except Exception as e:
            print(f"Error in DatasetTextsAPI: {e}")
            return Response({
                'error': str(e),
                'text_options': [],
                'total_texts': 0
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PerspectiveAnswersAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectStaffAndReadOnly]
    
    def get(self, request, *args, **kwargs):
        try:
            project_id = self.kwargs["project_id"]
            question_id = self.kwargs["question_id"]
            
            print(f"Fetching answers for question {question_id} in project {project_id}")
            
            # Get the question
            question = get_object_or_404(Question, pk=question_id, project=project_id)
            
            print(f"Found question: '{question.text}' (type: {question.question_type})")
            
            # Get all answers for this question
            answers = Answer.objects.filter(question=question).select_related('user', 'selected_option')
            
            print(f"Found {answers.count()} answers")
            
            answer_list = []
            for answer in answers:
                answer_data = {
                    'id': answer.id,
                    'username': answer.user.username if answer.user else 'Unknown',
                    'createdAt': answer.created_at.isoformat() if hasattr(answer, 'created_at') else None
                }
                
                # Add answer content based on question type
                if question.question_type == 'open':
                    # For open questions, get the text_answer field
                    text_response = answer.text_answer if answer.text_answer else 'No response'
                    answer_data['text'] = text_response
                    answer_data['selectedOption'] = None
                    print(f"Open answer from {answer.user.username}: '{text_response}'")
                else:  # closed/multiple choice
                    # For closed questions, get the selected option
                    if answer.selected_option:
                        answer_data['selectedOption'] = answer.selected_option.text
                        print(f"Closed answer from {answer.user.username}: '{answer.selected_option.text}'")
                    else:
                        answer_data['selectedOption'] = 'No option selected'
                        print(f"Closed answer from {answer.user.username}: No option selected")
                    
                    # For closed questions, text_answer might contain additional comments
                    answer_data['text'] = answer.text_answer if answer.text_answer else None
                
                answer_list.append(answer_data)
            
            response_data = {
                'question': {
                    'id': question.id,
                    'text': question.text,
                    'type': question.question_type
                },
                'answers': answer_list,
                'total_answers': len(answer_list)
            }
            
            print(f"Returning {len(answer_list)} answers")
            return Response(response_data)
            
        except Exception as e:
            print(f"Error in PerspectiveAnswersAPI: {e}")
            import traceback
            traceback.print_exc()
            return Response({
                'error': str(e),
                'answers': [],
                'total_answers': 0
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
