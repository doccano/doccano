from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Annotation
from .serializers import AnnotationSerializer
from examples.models import Example
from typing import Optional

class AnnotationView(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]  # enable filtering
    filterset_fields = ['dataset_item_id']   # allow filtering by dataset_item_id

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
            try:
                category_types_qs = project.category_types.all()
                category_types = list(category_types_qs.values("id", "text", "background_color"))
            except AttributeError:
                category_types = []
                
            meta_data = {}
            if hasattr(example, "meta") and example.meta:
                if isinstance(example.meta, dict):
                    meta_data = example.meta
                else:
                    try:
                        import json
                        meta_data = json.loads(example.meta)
                    except Exception as e:
                        print("Error parsing meta:", e)
                        meta_data = {}

            assigned_category = None
            assigned_category_raw = meta_data.get("category", None)
            if assigned_category_raw and isinstance(assigned_category_raw, str):
                for ct in category_types:
                    if ct["text"] == assigned_category_raw:
                        assigned_category = ct
                        break

            if not assigned_category and hasattr(example, "categories") and example.categories.exists():
                assigned_category = list(example.categories.values("id", "text", "background_color"))[0]

            if not assigned_category:
                print(f"WARNING: No assigned category found for example {example.id}")
                for ct in category_types:
                    if ct["text"] == "Plush":
                        assigned_category = ct
                        print(f"Defaulting to Plush for example {example.id}")
                        break
                if not assigned_category:
                    assigned_category = {}

            aggregated = {
                "text": example.text,
                "categories": category_types,
                "assigned_category": assigned_category
            }
        else:
            aggregated = {
                "text": example.text
            }

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

async def getByDatasetItem(dataset_item_id: int) -> Optional[Annotation]:
    url = "/annotations/"
    response = await ApiService.get(url, {"params": {"dataset_item_id": dataset_item_id}})
    annotations = response.data.get("results", response.data)
    return annotations[0] if annotations else None