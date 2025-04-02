import hashlib
import json
from django.db import models
from django.conf import settings
from django.db.models import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

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

    def list_similar_annotations(self):
        """
        Returns a queryset of annotations that have:
          - the exact same additional_info["text"],
          - the same extracted_labels["text"] and extracted_labels["label"],
          - but a different extracted_labels["spans"].
        This identifies annotations made on different dataset items
        that use the same text and label but have different spans.
        """
        if not self.additional_info or 'text' not in self.additional_info:
            return Annotation.objects.none()
        text_val = self.additional_info['text']
        label_text = ""
        label_val = None
        current_spans = None
        if self.extracted_labels:
            label_text = self.extracted_labels.get("text", "")
            label_val = self.extracted_labels.get("label")
            current_spans = self.extracted_labels.get("spans")
        qs = Annotation.objects.filter(
            additional_info__text=text_val,
            extracted_labels__text=label_text,
            extracted_labels__label=label_val,
        ).exclude(id=self.id)
        if current_spans is not None:
            qs = qs.exclude(extracted_labels__spans=current_spans)
        return qs