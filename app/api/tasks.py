import itertools

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Document, Label, Project
from .serializers import DocumentSerializer, LabelSerializer
from .views.upload.exception import FileParseException
from .views.upload.factory import (get_data_class, get_dataset_class,
                                   get_label_class)
from .views.upload.utils import append_field


@shared_task
def injest_data(user_id, project_id, filenames, format: str, **kwargs):
    project = get_object_or_404(Project, pk=project_id)
    user = get_object_or_404(get_user_model(), pk=user_id)
    response = {'error': []}

    # Prepare dataset.
    dataset_class = get_dataset_class(format)
    dataset = dataset_class(
        filenames=filenames,
        label_class=get_label_class(project.project_type),
        data_class=get_data_class(project.project_type),
        **kwargs
    )
    annotation_serializer_class = project.get_annotation_serializer()
    it = iter(dataset)
    while True:
        try:
            example = next(it)
        except StopIteration:
            break
        except FileParseException as err:
            response['error'].append(err.dict())
            continue

        data_serializer = DocumentSerializer(data=example.data)
        if not data_serializer.is_valid():
            continue
        data = data_serializer.save(project=project)

        stored_labels = {label.text for label in project.labels.all()}
        labels = [label for label in example.label if label['text'] not in stored_labels]
        label_serializer = LabelSerializer(data=labels, many=True)
        if not label_serializer.is_valid():
            continue
        label_serializer.save(project=project)

        mapping = {label.text: label.id for label in project.labels.all()}
        annotation = example.annotation(mapping)
        append_field(annotation, document=data.id)
        annotation_serializer = annotation_serializer_class(
            data=annotation,
            many=True
        )
        if not annotation_serializer.is_valid():
            continue
        annotation_serializer.save(user=user)

    return response
