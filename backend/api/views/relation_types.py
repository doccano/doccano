import json

from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..exceptions import RelationTypesValidationError
from ..models import Project, RelationTypes
from ..permissions import IsInProjectReadOnlyOrAdmin, IsProjectAdmin
from ..serializers import RelationTypesSerializer


class RelationTypesList(generics.ListCreateAPIView):
    serializer_class = RelationTypesSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return project.relation_types

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        serializer.save(project=project)

    def delete(self, request, *args, **kwargs):
        delete_ids = request.data['ids']
        RelationTypes.objects.filter(pk__in=delete_ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RelationTypesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RelationTypes.objects.all()
    serializer_class = RelationTypesSerializer
    lookup_url_kwarg = 'relation_type_id'
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]


class RelationTypesUploadAPI(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if 'file' not in request.data:
            raise ParseError('Empty content')
        project = get_object_or_404(Project, pk=kwargs['project_id'])
        try:
            relation_types = json.load(request.data)
            serializer = RelationTypesSerializer(data=relation_types, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(project=project)
            return Response(status=status.HTTP_201_CREATED)
        except json.decoder.JSONDecodeError:
            raise ParseError('The file format is invalid.')
        except IntegrityError:
            raise RelationTypesValidationError


# class RelationTypesList(APIView):
#     permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]
#
#     def get(self, request, *args, **kwargs):
#         relation_types = RelationTypes.objects.all()
#         serializer = RelationTypesSerializer(relation_types, many=True)
#         return Response(serializer.data)
#
#     def get_by_id(self, request, *args, **kwargs):
#         id = json.load(request.data['id'])
#         logging.info(f"Requested:: {id}")
#         relation_type = RelationTypes.objects.get(pk=id)
#         serializer = RelationTypesSerializer(relation_type, many=True)
#         return Response(serializer.data)
#
#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         if 'file' not in request.data:
#             raise ParseError('Empty content')
#         # project = get_object_or_404(Project, pk=kwargs['project_id'])
#         try:
#             logging.info(f"request.data:: {request.data}")
#             relation_type = json.load(request.data['relation_type'])
#             serializer = RelationTypesSerializer(relation_type, many=False)
#             serializer.is_valid(raise_exception=True)
#             # serializer.save(project=project)
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)
#         except json.decoder.JSONDecodeError:
#             raise ParseError('The file format is invalid.')
#         except IntegrityError:
#             raise RelationTypesValidationError
