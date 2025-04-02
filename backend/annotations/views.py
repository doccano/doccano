from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Annotation
from .serializers import AnnotationSerializer
from examples.models import Example

class AnnotationView(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = [IsAuthenticated]

    def aggregate_extracted_labels(self, dataset_item_id, request):
        example = Example.objects.get(id=dataset_item_id)
        project = example.project

        project_type = getattr(project, 'projectType', None)
        if project_type is None:
            if project.__class__.__name__ == "SequenceLabelingProject":
                project_type = "SequenceLabeling"
            elif project.__class__.__name__ == "DocumentClassificationProject":
                project_type = "DocumentClassification"
            else:
                project_type = "Unknown"

        if project_type == "SequenceLabeling":
            if hasattr(example, "get_spans_json") and callable(example.get_spans_json):
                spans = example.get_spans_json()
            elif hasattr(example, "spans"):
                spans = list(example.spans.values("start_offset", "end_offset", "label"))
            else:
                spans = []

            try:
                span_types_qs = project.span_types.all()
            except AttributeError:
                span_types_qs = project.spantype_set.all()
            label_types = list(span_types_qs.values("id", "text", "background_color"))

            aggregated = {
                "text": example.text,
                "spans": spans,
                "labelTypes": label_types
            }
        elif project_type == "DocumentClassification":
            aggregated = {
                "text": example.text,
                "label": example.meta.get("category") if example.meta else ""
            }
        else:
            aggregated = {"text": example.text}

        return aggregated

    def perform_create(self, serializer):
        dataset_item_id = serializer.validated_data.get("dataset_item_id")
        new_labels = self.aggregate_extracted_labels(dataset_item_id, self.request)
        serializer.save(
            annotator=self.request.user,
            extracted_labels=new_labels
        )

    def perform_update(self, serializer):
        dataset_item_id = serializer.validated_data.get("dataset_item_id")
        new_labels = self.aggregate_extracted_labels(dataset_item_id, self.request)
        serializer.save(extracted_labels=new_labels)