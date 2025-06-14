from rest_framework import serializers
from .models import Question, QuestionOption, Answer, QuestionType


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['id', 'text', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, required=False)
    answer_count = serializers.SerializerMethodField()
    user_answered = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'is_required', 'order', 'options', 'answer_count', 'user_answered', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_answer_count(self, obj):
        return obj.answers.count()

    def get_user_answered(self, obj):
        # Check if specific target user is provided in context
        target_user = self.context.get('target_user')
        if target_user:
            return obj.answers.filter(user=target_user).exists()
        
        # Fall back to request user
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.answers.filter(user=request.user).exists()
        return False

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        question = Question.objects.create(**validated_data)
        
        if question.question_type == QuestionType.CLOSED:
            for option_data in options_data:
                QuestionOption.objects.create(question=question, **option_data)
        
        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options', [])
        
        # Update question fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update options for closed questions
        if instance.question_type == QuestionType.CLOSED:
            # Delete existing options
            instance.options.all().delete()
            # Create new options
            for option_data in options_data:
                QuestionOption.objects.create(question=instance, **option_data)
        
        return instance


class BulkQuestionSerializer(serializers.Serializer):
    questions = QuestionSerializer(many=True)

    def create(self, validated_data):
        questions_data = validated_data['questions']
        questions = []
        
        for question_data in questions_data:
            options_data = question_data.pop('options', [])
            question = Question.objects.create(**question_data)
            
            if question.question_type == QuestionType.CLOSED:
                for option_data in options_data:
                    QuestionOption.objects.create(question=question, **option_data)
            
            questions.append(question)
        
        return questions


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'text_answer', 'selected_option', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        question = data['question']
        
        if question.question_type == QuestionType.OPEN:
            if not data.get('text_answer'):
                raise serializers.ValidationError("Text answer is required for open questions.")
            if data.get('selected_option'):
                raise serializers.ValidationError("Selected option should not be set for open questions.")
        elif question.question_type == QuestionType.CLOSED:
            if not data.get('selected_option'):
                raise serializers.ValidationError("Selected option is required for closed questions.")
            if data.get('text_answer'):
                raise serializers.ValidationError("Text answer should not be set for closed questions.")
            if data['selected_option'].question != question:
                raise serializers.ValidationError("Selected option must belong to the same question.")
        
        return data

    def create(self, validated_data):
        # Add user from request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
