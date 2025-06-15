from rest_framework import viewsets, status, generics, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from projects.models import Project, Member
from .models import Question, Answer
from .serializers import (
    QuestionSerializer, 
    BulkQuestionSerializer, 
    AnswerSerializer
)
from .permissions import CanCreatePerspective, CanAnswerPerspective, CanViewPerspective


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['question_type', 'is_required']
    ordering_fields = ['order', 'created_at']
    ordering = ['order', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_create', 'bulk_delete', 'delete_all']:
            permission_classes = [IsAuthenticated, CanCreatePerspective]
        else:
            permission_classes = [IsAuthenticated, CanViewPerspective]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        queryset = Question.objects.filter(project_id=project_id)
        
        # Filter by member_id if provided
        member_id = self.request.query_params.get('member_id')
        answered_filter = self.request.query_params.get('answered')
        
        if member_id:
            # Validate that member_id belongs to the project
            member = get_object_or_404(Member, id=member_id, project_id=project_id)
            
            if answered_filter == 'true':
                # Return only questions the member has answered
                answered_question_ids = Answer.objects.filter(
                    question__project_id=project_id,
                    user=member.user
                ).values_list('question_id', flat=True)
                queryset = queryset.filter(id__in=answered_question_ids)
            elif answered_filter == 'false':
                # Return only questions the member has NOT answered
                answered_question_ids = Answer.objects.filter(
                    question__project_id=project_id,
                    user=member.user
                ).values_list('question_id', flat=True)
                queryset = queryset.exclude(id__in=answered_question_ids)
        
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        member_id = self.request.query_params.get('member_id')
        if member_id:
            try:
                member = Member.objects.get(id=member_id, project_id=self.kwargs['project_id'])
                context['target_user'] = member.user
                
                # Include answers for admin users (for filtering purposes)
                if member.is_admin():
                    context['include_answers'] = True
                    
            except Member.DoesNotExist:
                pass
        return context

    def list(self, request, *args, **kwargs):
        # Require member_id for list view
        member_id = request.query_params.get('member_id')
        if not member_id:
            return Response(
                {'error': 'member_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate member exists in project
        try:
            Member.objects.get(id=member_id, project_id=kwargs['project_id'])
        except Member.DoesNotExist:
            return Response(
                {'error': 'Member not found in this project'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Override destroy to ensure consistent response format"""
        instance = self.get_object()
        question_text = instance.text[:50] + "..." if len(instance.text) > 50 else instance.text
        self.perform_destroy(instance)
        return Response({
            'message': f'Question "{question_text}" deleted successfully'
        }, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        import logging
        logger = logging.getLogger(__name__)

        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        logger.info(f"Creating question for project {project.id}")
        logger.info(f"Request data: {self.request.data}")

        try:
            serializer.save(project=project, created_by=self.request.user)
            logger.info("Question created successfully")
        except Exception as e:
            logger.error(f"Error creating question: {e}")
            raise

    def perform_destroy(self, instance):
        """
        Delete question and reorder remaining questions to maintain sequential order
        """
        import logging
        logger = logging.getLogger(__name__)
        
        project = instance.project
        deleted_order = instance.order
        
        logger.info(f"Deleting question {instance.id} with order {deleted_order}")
        
        # Delete the question
        instance.delete()
        
        # Reorder remaining questions with order greater than deleted question
        questions_to_reorder = Question.objects.filter(
            project=project,
            order__gt=deleted_order
        ).order_by('order')
        
        logger.info(f"Reordering {questions_to_reorder.count()} questions after deletion")
        
        # Update order for each question (decrease by 1)
        for question in questions_to_reorder:
            question.order -= 1
            question.save(update_fields=['order'])
            logger.info(f"Updated question {question.id} order from {question.order + 1} to {question.order}")
        
        logger.info("Question deletion and reordering completed successfully")

    @action(detail=False, methods=['post'])
    def bulk_create(self, request, project_id=None):
        project = get_object_or_404(Project, pk=project_id)
        serializer = BulkQuestionSerializer(data=request.data)
        
        if serializer.is_valid():
            questions_data = serializer.validated_data['questions']
            for question_data in questions_data:
                question_data['project'] = project
                question_data['created_by'] = request.user
            
            questions = serializer.save()
            response_serializer = QuestionSerializer(questions, many=True, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def bulk_delete(self, request, project_id=None):
        question_ids = request.data.get('ids', [])
        if not question_ids:
            return Response({'error': 'No question IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        project = get_object_or_404(Project, pk=project_id)
        questions = Question.objects.filter(
            id__in=question_ids,
            project_id=project_id
        ).order_by('order')
        
        if not questions.exists():
            return Response({'error': 'No questions found to delete'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get the orders of questions to be deleted
        deleted_orders = list(questions.values_list('order', flat=True))
        deleted_count = questions.count()
        
        # Delete the questions
        questions.delete()
        
        # Reorder remaining questions
        self._reorder_questions_after_bulk_delete(project, deleted_orders)
        
        return Response({
            'message': f'{deleted_count} questions deleted successfully',
            'deleted_count': deleted_count
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def delete_all(self, request, project_id=None):
        """Delete all questions in the project"""
        questions = Question.objects.filter(project_id=project_id)
        deleted_count = questions.count()
        questions.delete()

        return Response({
            'message': f'{deleted_count} questions deleted successfully',
            'deleted_count': deleted_count
        }, status=status.HTTP_200_OK)

    def _reorder_questions_after_bulk_delete(self, project, deleted_orders):
        """
        Helper method to reorder questions after bulk deletion
        """
        import logging
        logger = logging.getLogger(__name__)
        
        # Sort deleted orders to process from lowest to highest
        deleted_orders.sort()
        
        logger.info(f"Reordering questions after bulk deletion of orders: {deleted_orders}")
        
        # Get all remaining questions ordered by their current order
        remaining_questions = Question.objects.filter(project=project).order_by('order')
        
        # Reassign orders sequentially starting from 1
        new_order = 1
        for question in remaining_questions:
            if question.order != new_order:
                old_order = question.order
                question.order = new_order
                question.save(update_fields=['order'])
                logger.info(f"Updated question {question.id} order from {old_order} to {new_order}")
            new_order += 1
        
        logger.info("Bulk deletion reordering completed successfully")

    @action(detail=False, methods=['post'])
    def reorder_all(self, request, project_id=None):
        """
        Manually reorder all questions in a project to have sequential orders
        """
        project = get_object_or_404(Project, pk=project_id)
        
        try:
            count = Question.reorder_all_questions(project)
            return Response({
                'message': f'Successfully reordered {count} questions',
                'reordered_count': count
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': f'Failed to reorder questions: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def answers(self, request, project_id=None, pk=None):
        """
        Get all answers for a specific question (without user information for confidentiality)
        """
        question = self.get_object()
        answers = Answer.objects.filter(question=question).order_by('-created_at')
        
        # Return only the answer content, not user information
        answer_data = []
        for answer in answers:
            if answer.text_answer:
                # Open text answer
                answer_data.append({
                    'id': answer.id,
                    'type': 'text',
                    'content': answer.text_answer,
                    'created_at': answer.created_at
                })
            elif answer.selected_option:
                # Multiple choice answer
                answer_data.append({
                    'id': answer.id,
                    'type': 'choice',
                    'content': answer.selected_option.text,
                    'created_at': answer.created_at
                })
        
        return Response({
            'question_id': question.id,
            'question_text': question.text,
            'question_type': question.question_type,
            'total_answers': len(answer_data),
            'answers': answer_data
        })


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    http_method_names = ['get', 'post', 'delete']  # Allow GET, POST and DELETE (sua funcionalidade)
    permission_classes = [IsAuthenticated, CanAnswerPerspective]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['question']

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Answer.objects.filter(
            question__project_id=project_id,
            user=self.request.user
        )

    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        
        # Check if user already answered this question (mesclando as duas mensagens)
        if Answer.objects.filter(question=question, user=self.request.user).exists():
            raise serializers.ValidationError("You have already answered this item.")
        
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # Only allow users to delete their own answers (sua funcionalidade)
        if instance.user != self.request.user:
            raise serializers.ValidationError("You can only delete your own answers.")
        
        instance.delete()


class ProjectQuestionStatsView(generics.RetrieveAPIView):
    """
    View to get statistics about questions and answers for a project.
    Only accessible by project admins.
    """
    permission_classes = [IsAuthenticated, CanCreatePerspective]

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        questions = Question.objects.filter(project=project)
        
        stats = {
            'total_questions': questions.count(),
            'total_answers': Answer.objects.filter(question__project=project).count(),
            'questions_with_answers': questions.filter(answers__isnull=False).distinct().count(),
            'questions': []
        }
        
        for question in questions:
            question_stats = {
                'id': question.id,
                'text': question.text,
                'question_type': question.question_type,
                'answer_count': question.answers.count(),
                'options': []
            }
            
            if question.question_type == 'closed':
                for option in question.options.all():
                    option_stats = {
                        'id': option.id,
                        'text': option.text,
                        'answer_count': Answer.objects.filter(selected_option=option).count()
                    }
                    question_stats['options'].append(option_stats)
            
            stats['questions'].append(question_stats)
        
        return Response(stats)
