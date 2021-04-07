import itertools

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Document, Label, Project
from .serializers import LabelSerializer, DocumentSerializer
from .views.upload.factory import get_data_class, get_dataset_class, get_label_class
from .views.upload.utils import append_field


@shared_task
def injest_data(user_id, project_id, filenames, format: str, **kwargs):
    project = get_object_or_404(Project, pk=project_id)
    user = get_object_or_404(get_user_model(), pk=user_id)
    data_class = get_data_class(project.project_type)
    dataset_class = get_dataset_class(format)
    label_class = get_label_class(project.project_type)
    dataset = dataset_class(
        filenames=filenames,
        label_class=label_class,
        data_class=data_class,
        **kwargs
    )
    annotation_serializer_class = project.get_annotation_serializer()
    for batch in dataset.batch(settings.IMPORT_BATCH_SIZE):
        data_serializer = DocumentSerializer(data=batch.data(), many=True)
        data_serializer.is_valid()
        data = data_serializer.save(project=project)

        label_serializer = LabelSerializer(data=batch.label(), many=True)
        label_serializer.is_valid()
        label_serializer.save(project=project)

        mapping = {label['text']: label['id'] for label in project.labels.values()}
        annotation = batch.annotation(mapping)
        for a, d in zip(annotation, data):
            append_field(a, document=d.id)
        annotation_serializer = annotation_serializer_class(
            data=list(itertools.chain(*annotation)),
            many=True
        )
        annotation_serializer.is_valid()
        annotation_serializer.save(user=user)

    return {'error': []}
