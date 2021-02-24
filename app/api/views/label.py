import json

from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Project, Label
from ..serializers import LabelSerializer
from ..permissions import IsInProjectReadOnlyOrAdmin, IsProjectAdmin


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
        labels = json.load(request.data['file'])
        project = get_object_or_404(Project, pk=kwargs['project_id'])
        try:
            for label in labels:
                serializer = LabelSerializer(data=label)
                serializer.is_valid(raise_exception=True)
                serializer.save(project=project)
            return Response(status=status.HTTP_201_CREATED)
        except IntegrityError:
            content = {'error': 'IntegrityError: you cannot create a label with same name or shortkey.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
