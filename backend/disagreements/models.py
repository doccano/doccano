from django.db import models
from django.conf import settings
from django.db.models import JSONField

class Disagreement(models.Model):
    dataset_item_id = models.IntegerField()
    signature = models.CharField(max_length=64, db_index=True)
  
    annotations = models.ManyToManyField("annotations.Annotation")
    
    disagreement_details = JSONField(null=True, blank=True)
   
    status = models.CharField(max_length=20, default="open")
   
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    resolution_comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Disagreement for dataset item {self.dataset_item_id} from {self.signature} (Status: {self.status})"