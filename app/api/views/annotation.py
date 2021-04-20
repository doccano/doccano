from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Document, Project
from ..permissions import (IsAnnotationApprover, IsInProjectOrAdmin,
                           IsOwnAnnotation, IsProjectAdmin)
from ..serializers import ApproverSerializer


class AnnotationList(generics.ListCreateAPIView):
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectOrAdmin]
    swagger_schema = None

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs['project_id'])

    def get_serializer_class(self):
        self.serializer_class = self.project.get_annotation_serializer()
        return self.serializer_class

    def get_queryset(self):
        model = self.project.get_annotation_class()
        queryset = model.objects.filter(document=self.kwargs['doc_id'])
        if not self.project.collaborative_annotation:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        if self.project.single_class_classification:
            self.get_queryset().delete()
        request.data['document'] = self.kwargs['doc_id']
        return super().create(request, args, kwargs)

    def perform_create(self, serializer):
        serializer.save(document_id=self.kwargs['doc_id'], user=self.request.user)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'annotation_id'
    swagger_schema = None

    def get_permissions(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        if project.collaborative_annotation:
            self.permission_classes = [IsAuthenticated & IsInProjectOrAdmin]
        else:
            self.permission_classes = [IsAuthenticated & IsInProjectOrAdmin & IsOwnAnnotation]
        return super().get_permissions()

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = project.get_annotation_serializer()
        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        model = project.get_annotation_class()
        self.queryset = model.objects.all()
        return self.queryset


class ApproveLabelsAPI(APIView):
    permission_classes = [IsAuthenticated & (IsAnnotationApprover | IsProjectAdmin)]

    def post(self, request, *args, **kwargs):
        approved = self.request.data.get('approved', True)
        document = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        document.annotations_approved_by = self.request.user if approved else None
        document.save()
        return Response(ApproverSerializer(document).data)
