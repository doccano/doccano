import json
import re

from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import LabelValidationError
from .models import CategoryType, LabelType, RelationType, SpanType
from .serializers import (
    CategoryTypeSerializer,
    LabelSerializer,
    RelationTypeSerializer,
    SpanTypeSerializer,
)
from projects.models import Project
from projects.permissions import (
    IsProjectAdmin,
    IsProjectMember,
    IsProjectStaffAndReadOnly,
)


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def camel_to_snake_dict(d):
    return {camel_to_snake(k): v for k, v in d.items()}


class LabelList(generics.ListCreateAPIView):
    model = LabelType
    filter_backends = [DjangoFilterBackend]
    serializer_class = LabelSerializer
    pagination_class = None

    def get_permissions(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        if project.allow_member_to_create_label_type and self.request.method == "POST":
            self.permission_classes = [IsAuthenticated & IsProjectMember]
        else:
            self.permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]
        return super().get_permissions()

    def get_queryset(self):
        return self.model.objects.filter(project=self.kwargs["project_id"])

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs["project_id"])

    def delete(self, request, *args, **kwargs):
        delete_ids = request.data["ids"]
        self.model.objects.filter(pk__in=delete_ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryTypeList(LabelList):
    model = CategoryType
    serializer_class = CategoryTypeSerializer


class CategoryTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoryType.objects.all()
    serializer_class = CategoryTypeSerializer
    lookup_url_kwarg = "label_id"
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]


class SpanTypeList(LabelList):
    model = SpanType
    serializer_class = SpanTypeSerializer


class SpanTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpanType.objects.all()
    serializer_class = SpanTypeSerializer
    lookup_url_kwarg = "label_id"
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]


class RelationTypeList(LabelList):
    model = RelationType
    serializer_class = RelationTypeSerializer


class RelationTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RelationType.objects.all()
    serializer_class = RelationTypeSerializer
    lookup_url_kwarg = "label_id"
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]


class LabelUploadAPI(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    serializer_class = LabelSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if "file" not in request.data:
            raise ParseError("Empty content")
        try:
            labels = json.load(request.data["file"])
            labels = list(map(camel_to_snake_dict, labels))
            serializer = self.serializer_class(data=labels, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(project_id=kwargs["project_id"])
            return Response(status=status.HTTP_201_CREATED)
        except json.decoder.JSONDecodeError:
            raise ParseError("The file format is invalid.")
        except IntegrityError:
            raise LabelValidationError


class CategoryTypeUploadAPI(LabelUploadAPI):
    serializer_class = CategoryTypeSerializer


class SpanTypeUploadAPI(LabelUploadAPI):
    serializer_class = SpanTypeSerializer


class RelationTypeUploadAPI(LabelUploadAPI):
    serializer_class = RelationTypeSerializer
