import json

from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from labels.serializers import AnnotationRelationsSerializer
from members.permissions import IsProjectAdmin

from ...exceptions import AnnotationRelationValidationError
from ...models import Project


class RelationUploadAPI(APIView):
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
