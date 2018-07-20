import json

from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from rest_framework import viewsets, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models.query import QuerySet


from .models import Label, Document, Project
from .models import DocumentAnnotation, SequenceAnnotation
from .serializers import LabelSerializer, ProjectSerializer, DocumentSerializer, DocumentAnnotationSerializer
from .serializers import SequenceSerializer, SequenceAnnotationSerializer


class IndexView(TemplateView):
    template_name = 'index.html'


class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'annotation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = kwargs.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        if project.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            self.template_name = 'annotation/document_classification.html'
        elif project.is_type_of(Project.SEQUENCE_LABELING):
            self.template_name = 'annotation/sequence_labeling.html'
        elif project.is_type_of(Project.Seq2seq):
            self.template_name = 'annotation/seq2seq.html'
        else:
            pass

        return context


class ProjectsView(LoginRequiredMixin, ListView):
    model = Project
    paginate_by = 100
    template_name = 'projects.html'


class ProjectAdminView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project_admin.html'


class RawDataAPI(View):

    def post(self, request, *args, **kwargs):
        """Upload data."""
        f = request.FILES['file']
        content = ''.join(chunk.decode('utf-8') for chunk in f.chunks())
        for line in content.split('\n'):
            j = json.loads(line)
            Document(text=j['text']).save()

        return JsonResponse({'status': 'ok'})


class DataDownloadAPI(View):

    def get(self, request, *args, **kwargs):
        annotated_docs = [a.as_dict() for a in Annotation.objects.filter(manual=True)]
        json_str = json.dumps(annotated_docs)
        response = HttpResponse(json_str, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=annotation_data.json'

        return response


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(methods=['get'], detail=True)
    def progress(self, request, pk=None):
        project = self.get_object()
        docs = project.documents.all()
        if project.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            remaining = docs.filter(doc_annotations__isnull=True).count()
        elif project.is_type_of(Project.SEQUENCE_LABELING):
            remaining = docs.filter(seq_annotations__isnull=True).count()
        elif project.is_type_of(Project.Seq2seq):
            remaining = docs.filter(seq2seq_annotations__isnull=True).count()
        else:
            remaining = 0
        return Response({'total': docs.count(), 'remaining': remaining})


class ProjectLabelsAPI(generics.ListCreateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    pagination_class = None

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        queryset = self.queryset.filter(project=project_id)

        return queryset

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)
        serializer.save(project=project)


class ProjectLabelAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        queryset = self.queryset.filter(project=project_id)

        return queryset

    def get_object(self):
        label_id = self.kwargs['label_id']
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=label_id)
        self.check_object_permissions(self.request, obj)

        return obj


class ProjectDocsAPI(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('text', )

    def get_serializer_class(self):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)
        if project.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            self.serializer_class = DocumentSerializer
        elif project.is_type_of(Project.SEQUENCE_LABELING):
            self.serializer_class = SequenceSerializer

        return self.serializer_class

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        queryset = self.queryset.filter(project=project_id)

        return queryset


class AnnotationsAPI(generics.ListCreateAPIView):
    #queryset = DocumentAnnotation.objects.all()
    #queryset = SequenceAnnotation.objects.all()
    #serializer_class = DocumentAnnotationSerializer
    pagination_class = None

    def get_serializer_class(self):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)
        if project.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            self.serializer_class = DocumentAnnotationSerializer
        elif project.is_type_of(Project.SEQUENCE_LABELING):
            self.serializer_class = SequenceAnnotationSerializer

        return self.serializer_class

    def get_queryset(self):
        doc_id = self.kwargs['doc_id']
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)
        if project.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            self.queryset = DocumentAnnotation.objects.all()
        elif project.is_type_of(Project.SEQUENCE_LABELING):
            self.queryset = SequenceAnnotation.objects.all()
        queryset = self.queryset.filter(document=doc_id)

        return queryset

    def post(self, request, *args, **kwargs):
        doc = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        label = get_object_or_404(Label, pk=request.data['label_id'])
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        if project.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            self.serializer_class = DocumentAnnotationSerializer
            annotation = DocumentAnnotation(document=doc, label=label, manual=True,
                                            user=self.request.user)
        elif project.is_type_of(Project.SEQUENCE_LABELING):
            self.serializer_class = SequenceAnnotationSerializer
            annotation = SequenceAnnotation(document=doc, label=label, manual=True,
                                            user=self.request.user,
                                            start_offset=request.data['start_offset'],
                                            end_offset=request.data['end_offset'])
        annotation.save()
        serializer = self.serializer_class(annotation)

        return Response(serializer.data)


class AnnotationAPI(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        doc_id = self.kwargs['doc_id']
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)
        if project.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            self.queryset = DocumentAnnotation.objects.all()
        elif project.is_type_of(Project.SEQUENCE_LABELING):
            self.queryset = SequenceAnnotation.objects.all()
        queryset = self.queryset.filter(document=doc_id)

        return queryset

    def get_object(self):
        annotation_id = self.kwargs['annotation_id']
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=annotation_id)
        self.check_object_permissions(self.request, obj)

        return obj
