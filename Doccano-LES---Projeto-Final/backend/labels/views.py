from functools import partial
from typing import Type

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import DiscrepancyMessage
from .serializers import DiscrepancyMessageSerializer
from projects.permissions import IsProjectMember
from projects.models import Project
from examples.models import Example

from .permissions import CanEditLabel
from .serializers import (
    BoundingBoxSerializer,
    CategorySerializer,
    RelationSerializer,
    SegmentationSerializer,
    SpanSerializer,
    TextLabelSerializer,
)
from labels.models import (
    BoundingBox,
    Category,
    Label,
    Relation,
    Segmentation,
    Span,
    TextLabel,
)


class BaseListAPI(generics.ListCreateAPIView):
    label_class: Type[Label]
    pagination_class = None
    permission_classes = [IsAuthenticated & IsProjectMember]
    swagger_schema = None

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_id"])

    def get_queryset(self):
        queryset = self.label_class.objects.filter(example=self.kwargs["example_id"])
        if not self.project.collaborative_annotation:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data["example"] = self.kwargs["example_id"]
        try:
            response = super().create(request, args, kwargs)
        except ValidationError as err:
            response = Response({"detail": err.messages}, status=status.HTTP_400_BAD_REQUEST)
        return response

    def perform_create(self, serializer):
        serializer.save(example_id=self.kwargs["example_id"], user=self.request.user)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DiscrepancyMessageListAPI(generics.ListCreateAPIView):
    serializer_class = DiscrepancyMessageSerializer
    permission_classes = [permissions.IsAuthenticated & IsProjectMember]
    pagination_class = None

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_id"])

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        print(f"Recuperando mensagens do chat - Project ID: {project_id}")
        print(f"Request path: {self.request.path}")
        print(f"Request user: {self.request.user}")
        print(f"Request kwargs: {self.kwargs}")
        
        # Verifica se o projeto existe
        project = get_object_or_404(Project, pk=project_id)
        
        queryset = DiscrepancyMessage.objects.filter(project_id=project_id)
        print(f"Query SQL: {queryset.query}")
        print(f"Encontradas {queryset.count()} mensagens")
        for msg in queryset:
            print(f"Message {msg.id}: {msg.text} by {msg.user} at {msg.created_at}")
        return queryset

    def perform_create(self, serializer):
        project_id = self.kwargs["project_id"]
        print(f"Criando nova mensagem no chat - Project ID: {project_id}, User: {self.request.user}")
        
        # Verifica se o projeto existe antes de criar a mensagem
        project = get_object_or_404(Project, pk=project_id)
        
        serializer.save(
            project_id=project_id,
            user=self.request.user
        )
        print("Mensagem criada com sucesso")

class BaseDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "annotation_id"
    swagger_schema = None

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_id"])

    def get_permissions(self):
        if self.project.collaborative_annotation:
            self.permission_classes = [IsAuthenticated & IsProjectMember]
        else:
            self.permission_classes = [IsAuthenticated & IsProjectMember & partial(CanEditLabel, self.queryset)]
        return super().get_permissions()


class CategoryListAPI(BaseListAPI):
    label_class = Category
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        if self.project.single_class_classification:
            self.get_queryset().delete()
        return super().create(request, args, kwargs)


class CategoryDetailAPI(BaseDetailAPI):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SpanListAPI(BaseListAPI):
    label_class = Span
    serializer_class = SpanSerializer


class SpanDetailAPI(BaseDetailAPI):
    queryset = Span.objects.all()
    serializer_class = SpanSerializer


class TextLabelListAPI(BaseListAPI):
    label_class = TextLabel
    serializer_class = TextLabelSerializer


class TextLabelDetailAPI(BaseDetailAPI):
    queryset = TextLabel.objects.all()
    serializer_class = TextLabelSerializer


class RelationList(BaseListAPI):
    label_class = Relation
    serializer_class = RelationSerializer


class RelationDetail(BaseDetailAPI):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer


class BoundingBoxListAPI(BaseListAPI):
    label_class = BoundingBox
    serializer_class = BoundingBoxSerializer


class BoundingBoxDetailAPI(BaseDetailAPI):
    queryset = BoundingBox.objects.all()
    serializer_class = BoundingBoxSerializer


class SegmentationListAPI(BaseListAPI):
    label_class = Segmentation
    serializer_class = SegmentationSerializer


class SegmentationDetailAPI(BaseDetailAPI):
    queryset = Segmentation.objects.all()
    serializer_class = SegmentationSerializer
