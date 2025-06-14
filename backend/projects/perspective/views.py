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
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_create', 'bulk_delete']:
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

    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request, project_id=None):
        question_ids = request.data.get('ids', [])
        if not question_ids:
            return Response({'error': 'No question IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        questions = Question.objects.filter(
            id__in=question_ids,
            project_id=project_id
        )
        
        deleted_count = questions.count()
        questions.delete()
        
        return Response({
            'message': f'{deleted_count} questions deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    http_method_names = ['get', 'post']  # Only allow GET and POST
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
        
        # Check if user already answered this question
        if Answer.objects.filter(question=question, user=self.request.user).exists():
            raise serializers.ValidationError("You have already answered this question.")
        
        serializer.save()


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
