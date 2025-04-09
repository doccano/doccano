from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from examples.models import Example
from labels.models import Span, Category
from annotations.models import Annotation
from annotations.views import AnnotationView

def update_annotation_for_example(example_id):
    view = AnnotationView()
    new_labels = view.aggregate_extracted_labels(example_id, None)
    Annotation.objects.filter(dataset_item_id=example_id).update(extracted_labels=new_labels)

@receiver(post_save, sender=Example)
def on_example_save(sender, instance, **kwargs):
    update_annotation_for_example(instance.id)

@receiver(post_save, sender=Span)
def on_span_save(sender, instance, **kwargs):
    update_annotation_for_example(instance.example.id)

@receiver(post_delete, sender=Span)
def on_span_delete(sender, instance, **kwargs):
    update_annotation_for_example(instance.example.id)

@receiver(post_save, sender=Category)
def on_category_save(sender, instance, **kwargs):
    if hasattr(instance, "example") and instance.example:
        update_annotation_for_example(instance.example.id)

@receiver(post_delete, sender=Category)
def on_category_delete(sender, instance, **kwargs):
    if hasattr(instance, "example") and instance.example:
        update_annotation_for_example(instance.example.id)