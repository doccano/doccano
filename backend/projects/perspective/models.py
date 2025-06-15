from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from projects.models import Project


class QuestionType(models.TextChoices):
    OPEN = "open", "Open Text"
    CLOSED = "closed", "Multiple Choice"


class DataType(models.TextChoices):
    STRING = "string", "String"
    INTEGER = "integer", "Integer"


class Question(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="perspective_questions")
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QuestionType.choices)
    data_type = models.CharField(max_length=10, choices=DataType.choices, blank=True, null=True)
    is_required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ['project', 'order']

    def __str__(self):
        return f"{self.project.name} - {self.text[:50]}"

    @classmethod
    def get_next_order(cls, project):
        """Get the next available order for a project"""
        max_order = cls.objects.filter(project=project).aggregate(
            models.Max('order')
        )['order__max']
        return (max_order or 0) + 1

    @classmethod
    def reorder_all_questions(cls, project):
        """
        Reorder all questions in a project to have sequential orders starting from 1
        """
        questions = cls.objects.filter(project=project).order_by('order')
        
        for index, question in enumerate(questions, start=1):
            if question.order != index:
                question.order = index
                question.save(update_fields=['order'])
        
        return questions.count()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        # If this is a new question, ensure we have a valid order
        if is_new:
            if not self.order or self.order == 0:
                self.order = self.get_next_order(self.project)
            else:
                # Check if the order is already taken
                if Question.objects.filter(project=self.project, order=self.order).exists():
                    self.order = self.get_next_order(self.project)
        
        super().save(*args, **kwargs)
        
        # If question is updated (not new), reset all answers
        if not is_new:
            self.answers.all().delete()


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['question', 'order']

    def __str__(self):
        return f"{self.question.text[:30]} - {self.text}"

    def clean(self):
        if self.question.question_type != QuestionType.CLOSED:
            raise ValidationError("Options can only be added to closed questions.")


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True, null=True)
    selected_option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['question', 'user']

    def __str__(self):
        return f"{self.question.text[:30]} - {self.user.username}"

    def clean(self):
        if self.question.question_type == QuestionType.OPEN:
            if not self.text_answer:
                raise ValidationError("Text answer is required for open questions.")
            if self.selected_option:
                raise ValidationError("Selected option should not be set for open questions.")
        elif self.question.question_type == QuestionType.CLOSED:
            if not self.selected_option:
                raise ValidationError("Selected option is required for closed questions.")
            if self.text_answer:
                raise ValidationError("Text answer should not be set for closed questions.")
            if self.selected_option.question != self.question:
                raise ValidationError("Selected option must belong to the same question.")
