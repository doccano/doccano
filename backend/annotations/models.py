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

@receiver(post_save, sender=Annotation)
def create_or_update_disagreement(sender, instance, created, **kwargs):
    if not created:
        return

    if not instance.additional_info or 'text' not in instance.additional_info:
        return

    text_val = instance.additional_info['text']
    snippet = text_val[:100]

    labels_json = json.dumps(instance.extracted_labels, sort_keys=True) if instance.extracted_labels else ''
    signature_source = f"{instance.dataset_item_id}:{text_val}:{labels_json}"
    signature = hashlib.sha256(signature_source.encode('utf-8')).hexdigest()

    similar_annotations = Annotation.objects.filter(
        dataset_item_id=instance.dataset_item_id,
        extracted_labels=instance.extracted_labels,
        additional_info__text=text_val
    ).exclude(id=instance.id)

    if similar_annotations.exists():
        Disagreement = apps.get_model('disagreements', 'Disagreement')
        disagreement, _ = Disagreement.objects.get_or_create(
            dataset_item_id=instance.dataset_item_id,
            signature=signature,
            defaults={'disagreement_details': snippet}
        )
        disagreement.annotations.add(instance)
        for ann in similar_annotations:
            disagreement.annotations.add(ann)