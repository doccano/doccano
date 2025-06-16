from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, time
from projects.models import Project
from projects.permissions import IsProjectAdmin, IsProjectMember
from .models import VotingConfiguration, AnnotationRule, Vote
from .serializers import (
    VotingConfigurationSerializer, 
    VotingConfigurationWriteSerializer,
    VoteSerializer, 
    VoteWriteSerializer,
    VotingResultsSerializer,
    UserVoteStatusSerializer
)


class VotingConfigurationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing voting configurations"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return VotingConfiguration.objects.filter(project_id=project_id).prefetch_related('annotation_rules')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VotingConfigurationWriteSerializer
        return VotingConfigurationSerializer
    
    def get_permissions(self):
        """
        Admin permissions for create, update, delete
        Member permissions for read and vote actions
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsProjectAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated, IsProjectMember]
        
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, id=project_id)
        serializer.save(project=project)
    
    @action(detail=True, methods=['get'], url_path='results')
    def get_results(self, request, project_id=None, pk=None):
        """Get aggregated voting results for a configuration"""
        
        configuration = self.get_object()
        results = []
        
        for rule in configuration.annotation_rules.all():
            vote_counts = rule.votes.aggregate(
                total=Count('id'),
                approve=Count('id', filter=Q(vote='approve')),
                disapprove=Count('id', filter=Q(vote='disapprove')),
                neutral=Count('id', filter=Q(vote='neutral'))
            )
            
            total_votes = vote_counts['total'] or 0
            approve_votes = vote_counts['approve'] or 0
            approval_percentage = (approve_votes / total_votes * 100) if total_votes > 0 else 0
            
            results.append({
                'rule_id': rule.id,
                'rule_name': rule.name,
                'total_votes': total_votes,
                'approve_votes': approve_votes,
                'disapprove_votes': vote_counts['disapprove'] or 0,
                'neutral_votes': vote_counts['neutral'] or 0,
                'approval_percentage': round(approval_percentage, 1)
            })
        
        serializer = VotingResultsSerializer(results, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='user-votes')
    def get_user_votes(self, request, project_id=None, pk=None):
        """Get current user's votes for a configuration"""
        
        configuration = self.get_object()
        user_votes = Vote.objects.filter(
            annotation_rule__voting_configuration=configuration,
            user=request.user
        ).select_related('annotation_rule')
        
        serializer = UserVoteStatusSerializer(user_votes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='vote')
    def vote(self, request, project_id=None, pk=None):
        """Submit or update a vote for an annotation rule"""
        
        configuration = self.get_object()
        rule_id = request.data.get('rule_id')
        vote_value = request.data.get('vote')
        
        if not rule_id:
            return Response({'error': 'rule_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not vote_value:
            return Response({'error': 'vote is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate rule belongs to configuration
        try:
            rule = configuration.annotation_rules.get(id=rule_id)
        except AnnotationRule.DoesNotExist:
            return Response({'error': 'Rule not found in this configuration'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if voting is active
        if not self._is_voting_active(configuration):
            return Response({'error': 'Voting is not currently active'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check voting method compatibility
        if not self._is_vote_allowed(configuration, vote_value):
            return Response({'error': f'Vote type "{vote_value}" not allowed for this voting method'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Create or update vote
        vote, created = Vote.objects.update_or_create(
            annotation_rule=rule,
            user=request.user,
            defaults={'vote': vote_value}
        )
        
        serializer = VoteSerializer(vote)
        action_text = 'created' if created else 'updated'
        
        return Response({
            'message': f'Vote {action_text} successfully',
            'vote': serializer.data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'], url_path='vote/(?P<rule_id>[^/.]+)')
    def remove_vote(self, request, project_id=None, pk=None, rule_id=None):
        """Remove a user's vote for an annotation rule"""
        
        configuration = self.get_object()
        
        try:
            rule = configuration.annotation_rules.get(id=rule_id)
            vote = Vote.objects.get(annotation_rule=rule, user=request.user)
            vote.delete()
            return Response({'message': 'Vote removed successfully'}, status=status.HTTP_204_NO_CONTENT)
        except AnnotationRule.DoesNotExist:
            return Response({'error': 'Rule not found'}, status=status.HTTP_404_NOT_FOUND)
        except Vote.DoesNotExist:
            return Response({'error': 'Vote not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'], url_path='active')
    def get_active(self, request, project_id=None):
        """Get currently active voting configurations for users"""
        
        now = timezone.now()
        current_date = now.date()
        current_time = now.time()
        
        active_configs = []
        for config in self.get_queryset():
            if self._is_voting_active(config, current_date, current_time):
                active_configs.append(config)
        
        serializer = self.get_serializer(active_configs, many=True)
        return Response(serializer.data)
    
    def _is_voting_active(self, configuration, current_date=None, current_time=None):
        """Check if voting is currently active for a configuration"""
        
        if current_date is None or current_time is None:
            now = timezone.now()
            current_date = now.date()
            current_time = now.time()
        
        # Check date range
        if current_date < configuration.start_date or current_date > configuration.end_date:
            return False
        
        # Check time range on start date
        if current_date == configuration.start_date and current_time < configuration.start_time:
            return False
        
        # Check time range on end date
        if current_date == configuration.end_date and current_time >= configuration.end_time:
            return False
        
        return True
    
    def _is_vote_allowed(self, configuration, vote_value):
        """Check if the vote type is allowed for the voting method"""
        
        if configuration.voting_method == 'approve_only':
            return vote_value in ['approve', 'neutral']
        elif configuration.voting_method == 'disapprove_only':
            return vote_value in ['disapprove', 'neutral']
        elif configuration.voting_method == 'approve_disapprove':
            return vote_value in ['approve', 'disapprove', 'neutral']
        
        return False
