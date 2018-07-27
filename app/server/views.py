import json

from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser


from .models import Label, Document, Project, Factory
from .models import DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation
from .serializers import LabelSerializer, ProjectSerializer


class IndexView(TemplateView):
    template_name = 'index.html'


class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'annotation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = kwargs.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        self.template_name = Factory.get_template(project)

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
    pagination_class = None

    @action(methods=['get'], detail=True)
    def progress(self, request, pk=None):
        project = self.get_object()
        docs = Factory.get_documents(project, is_null=True)
        total = project.documents.count()
        remaining = docs.count()

        return Response({'total': total, 'remaining': remaining})


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
        self.serializer_class = Factory.get_project_serializer(project)

        return self.serializer_class

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        queryset = self.queryset.filter(project=project_id)
        if not self.request.query_params.get('is_checked'):
            return queryset

        project = get_object_or_404(Project, pk=project_id)
        is_null = self.request.query_params.get('is_checked') == 'true'
        queryset = Factory.get_documents(project, is_null).distinct()

        return queryset


class AnnotationsAPI(generics.ListCreateAPIView):
    pagination_class = None

    def get_serializer_class(self):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)
        self.serializer_class = Factory.get_annotation_serializer(project)

        return self.serializer_class

    def get_queryset(self):
        doc_id = self.kwargs['doc_id']
        document = get_object_or_404(Document, pk=doc_id)
        self.queryset = Factory.get_annotations_by_doc(document)

        return self.queryset

    def post(self, request, *args, **kwargs):
        doc = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        label = get_object_or_404(Label, pk=request.data['label_id'])
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = Factory.get_annotation_serializer(project)
        if project.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            annotation = DocumentAnnotation(document=doc, label=label, manual=True,
                                            user=self.request.user)
        elif project.is_type_of(Project.SEQUENCE_LABELING):
            annotation = SequenceAnnotation(document=doc, label=label, manual=True,
                                            user=self.request.user,
                                            start_offset=request.data['start_offset'],
                                            end_offset=request.data['end_offset'])
        elif project.is_type_of(Project.Seq2seq):
            annotation = Seq2seqAnnotation(document=doc, manual=True, user=self.request.user)
        annotation.save()
        serializer = self.serializer_class(annotation)

        return Response(serializer.data)


class AnnotationAPI(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        doc_id = self.kwargs['doc_id']
        document = get_object_or_404(Document, pk=doc_id)
        self.queryset = Factory.get_annotations_by_doc(document)

        return self.queryset

    def get_object(self):
        annotation_id = self.kwargs['annotation_id']
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=annotation_id)
        self.check_object_permissions(self.request, obj)

        return obj
