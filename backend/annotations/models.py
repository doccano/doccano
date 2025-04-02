from django.db import models
from django.conf import settings
from django.db.models import JSONField

class Annotation(models.Model):
   
    dataset_item_id = models.IntegerField()
    annotator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
   
    extracted_labels = JSONField(null=True, blank=True)
    additional_info = JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Annotation on dataset item {self.dataset_item_id} by {self.annotator}"