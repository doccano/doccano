from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Example, Project
from ..permissions import (IsAnnotationApprover, IsInProjectOrAdmin,
                           IsOwnAnnotation, IsProjectAdmin)
from ..serializers import ApproverSerializer, get_annotation_serializer


class AnnotationList(generics.ListCreateAPIView):
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectOrAdmin]
    swagger_schema = None

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs['project_id'])

    def get_serializer_class(self):
        self.serializer_class = get_annotation_serializer(task=self.project.project_type)
        return self.serializer_class

    def get_queryset(self):
        model = self.project.get_annotation_class()
        queryset = model.objects.filter(example=self.kwargs['doc_id'])
        if not self.project.collaborative_annotation:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        if self.project.single_class_classification:
            self.get_queryset().delete()
        request.data['example'] = self.kwargs['doc_id']
        return super().create(request, args, kwargs)

    def perform_create(self, serializer):
        serializer.save(example_id=self.kwargs['doc_id'], user=self.request.user)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'annotation_id'
    swagger_schema = None

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs['project_id'])

    def get_permissions(self):
        if self.project.collaborative_annotation:
            self.permission_classes = [IsAuthenticated & IsInProjectOrAdmin]
        else:
            self.permission_classes = [IsAuthenticated & IsInProjectOrAdmin & IsOwnAnnotation]
        return super().get_permissions()

    def get_serializer_class(self):
        self.serializer_class = get_annotation_serializer(task=self.project.project_type)
        return self.serializer_class

    def get_queryset(self):
        model = self.project.get_annotation_class()
        self.queryset = model.objects.all()
        return self.queryset


class ApprovalAPI(APIView):
    permission_classes = [IsAuthenticated & (IsAnnotationApprover | IsProjectAdmin)]

    def post(self, request, *args, **kwargs):
        approved = self.request.data.get('approved', True)
        example = get_object_or_404(Example, pk=self.kwargs['example_id'])
        example.annotations_approved_by = self.request.user if approved else None
        example.save()
        return Response(ApproverSerializer(example).data)
