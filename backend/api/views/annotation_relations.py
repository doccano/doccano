import json

from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..exceptions import AnnotationRelationValidationError
from ..models import AnnotationRelations, Project
from ..permissions import IsInProjectReadOnlyOrAdmin, IsProjectAdmin
from ..serializers import AnnotationRelationsSerializer


class AnnotationRelationsList(generics.ListCreateAPIView):
    serializer_class = AnnotationRelationsSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return project.annotation_relations

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        serializer.save(project=project)

    def delete(self, request, *args, **kwargs):
        delete_ids = request.data['ids']
        AnnotationRelations.objects.filter(pk__in=delete_ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnnotationRelationsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnnotationRelations.objects.all()
    serializer_class = AnnotationRelationsSerializer
    lookup_url_kwarg = 'annotation_relation_id'
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]


class AnnotationRelationsUploadAPI(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if 'file' not in request.data:
            raise ParseError('Empty content')
        project = get_object_or_404(Project, pk=kwargs['project_id'])
        try:
            annotation_relations = json.load(request.data)
            serializer = AnnotationRelationsSerializer(data=annotation_relations, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(project=project)
            return Response(status=status.HTTP_201_CREATED)
        except json.decoder.JSONDecodeError:
            raise ParseError('The file format is invalid.')
        except IntegrityError:
            raise AnnotationRelationValidationError
