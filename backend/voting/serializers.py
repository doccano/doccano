from rest_framework import serializers
from django.contrib.auth.models import User
from .models import VotingConfiguration, AnnotationRule, Vote


class AnnotationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationRule
        fields = ['id', 'name', 'description', 'order']


class VotingConfigurationSerializer(serializers.ModelSerializer):
    annotation_rules = AnnotationRuleSerializer(many=True, read_only=True)
    
    class Meta:
        model = VotingConfiguration
        fields = [
            'id', 'name', 'description', 'voting_method', 
            'start_date', 'end_date', 'start_time', 'end_time',
            'status', 'created_at', 'updated_at', 'annotation_rules'
        ]
        read_only_fields = ['created_at', 'updated_at']


class VotingConfigurationWriteSerializer(serializers.ModelSerializer):
    annotation_rules = AnnotationRuleSerializer(many=True, write_only=True)
    
    class Meta:
        model = VotingConfiguration
        fields = [
            'id', 'name', 'description', 'voting_method', 
            'start_date', 'end_date', 'start_time', 'end_time',
            'status', 'annotation_rules'
        ]
    
    def create(self, validated_data):
        annotation_rules_data = validated_data.pop('annotation_rules', [])
        voting_config = VotingConfiguration.objects.create(**validated_data)
        
        for rule_data in annotation_rules_data:
            AnnotationRule.objects.create(
                voting_configuration=voting_config,
                **rule_data
            )
        
        return voting_config
    
    def update(self, instance, validated_data):
        annotation_rules_data = validated_data.pop('annotation_rules', [])
        
        # Update voting configuration fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update annotation rules
        if annotation_rules_data:
            # Delete existing rules
            instance.annotation_rules.all().delete()
            
            # Create new rules
            for rule_data in annotation_rules_data:
                AnnotationRule.objects.create(
                    voting_configuration=instance,
                    **rule_data
                )
        
        return instance


class VoteSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Vote
        fields = ['id', 'annotation_rule', 'user', 'username', 'vote', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'username', 'created_at', 'updated_at']


class VoteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['annotation_rule', 'vote']
    
    def create(self, validated_data):
        # Set the user from the request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Only allow updating the vote, not the rule or user
        instance.vote = validated_data.get('vote', instance.vote)
        instance.save()
        return instance


class VotingResultsSerializer(serializers.Serializer):
    """Serializer for aggregated voting results"""
    
    rule_id = serializers.IntegerField()
    rule_name = serializers.CharField()
    total_votes = serializers.IntegerField()
    approve_votes = serializers.IntegerField()
    disapprove_votes = serializers.IntegerField()
    neutral_votes = serializers.IntegerField()
    approval_percentage = serializers.FloatField()
    
    
class UserVoteStatusSerializer(serializers.Serializer):
    """Serializer for user's voting status"""
    
    configuration_id = serializers.IntegerField(source='voting_configuration.id')
    rule_id = serializers.IntegerField(source='annotation_rule.id')
    vote = serializers.CharField()
    voted_at = serializers.DateTimeField(source='updated_at')
