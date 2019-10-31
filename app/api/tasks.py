from celery import shared_task
from rest_framework_csv.renderers import CSVRenderer

from .models import Project
from .utils import CSVPainter, JSONPainter, JSONLRenderer


@shared_task
def download_text(download_format, project_id):
    project = Project.objects.get(pk=project_id)
    documents = project.documents.all()

    # json1 format prints text labels while json format prints annotations with label ids
    # json1 format - "labels": [[0, 15, "PERSON"], ..]
    # json format - "annotations": [{"label": 5, "start_offset": 0, "end_offset": 2, "user": 1},..]
    if download_format == "json1":
        painter = JSONPainter()
        renderer = JSONLRenderer()
        labels = project.labels.all()
        data = painter.paint_labels(documents, labels)
    else:
        if download_format == 'csv':
            painter = CSVPainter()
            renderer = CSVRenderer()
        elif download_format == 'json':
            painter = JSONPainter()
            renderer = JSONLRenderer()
        else:
            raise NotImplementedError(download_format)

        data = painter.paint(documents)

    rendered = renderer.render(data)
    return rendered.decode('utf-8') if isinstance(rendered, bytes) else ''.join(rendered)
