from django.db import models
from django.conf import settings
from projects.models import Project
from django.db.models import JSONField

class Perspective(models.Model):
    CATEGORY_CHOICES = [
        ('cultural', 'Cultural'),
        ('technic', 'Technic'),
        ('subjective', 'Subjective'),
    ]
    
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    subject = models.CharField(max_length=255, default="Default Subject")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='subjective')
    text = models.TextField()
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="perspectives"
    )
    linkedAnnotations = JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
