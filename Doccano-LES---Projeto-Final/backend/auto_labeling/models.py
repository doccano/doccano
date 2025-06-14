from auto_labeling_pipeline.models import RequestModelFactory
from django.core.exceptions import ValidationError
from django.db import models

from projects.models import Project


class AutoLabelingConfig(models.Model):
    TASK_CHOICES = (("Category", "category"), ("Span", "span"), ("Text", "text"), ("Relation", "relation"))
    model_name = models.CharField(max_length=100)
    model_attrs = models.JSONField(default=dict)
    template = models.TextField(default="")
    label_mapping = models.JSONField(default=dict, blank=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="auto_labeling_config")
    task_type = models.CharField(max_length=100, choices=TASK_CHOICES)
    default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.model_name

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        try:
            RequestModelFactory.find(self.model_name)
        except NameError:
            message = f"The specified model name {self.model_name} does not exist."
            raise ValidationError(message)
        except Exception:
            message = "The attributes does not match the model."
            raise ValidationError(message)
