import json
import re

from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..exceptions import LabelValidationError
from ..models import Label, Project
from ..permissions import IsInProjectReadOnlyOrAdmin, IsProjectAdmin
from ..serializers import LabelSerializer


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def camel_to_snake_dict(d):
    return {camel_to_snake(k): v for k, v in d.items()}


class LabelList(generics.ListCreateAPIView):
    serializer_class = LabelSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return project.labels

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        serializer.save(project=project)

    def delete(self, request, *args, **kwargs):
        delete_ids = request.data['ids']
        Label.objects.filter(pk__in=delete_ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LabelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    lookup_url_kwarg = 'label_id'
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]


class LabelUploadAPI(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if 'file' not in request.data:
            raise ParseError('Empty content')
        project = get_object_or_404(Project, pk=kwargs['project_id'])
        try:
            labels = json.load(request.data['file'])
            labels = list(map(camel_to_snake_dict, labels))
            serializer = LabelSerializer(data=labels, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(project=project)
            return Response(status=status.HTTP_201_CREATED)
        except json.decoder.JSONDecodeError:
            raise ParseError('The file format is invalid.')
        except IntegrityError:
            raise LabelValidationError
