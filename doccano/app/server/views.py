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

from .models import Annotation, Label, Document, Project
from .serializers import LabelSerializer, ProjectSerializer, DocumentSerializer, AnnotationSerializer


class IndexView(TemplateView):
    template_name = 'index.html'


class InboxView(LoginRequiredMixin, TemplateView):
    template_name = 'annotation.html'


class ProjectsView(LoginRequiredMixin, ListView):
    model = Project
    paginate_by = 100
    template_name = 'projects.html'


class ProjectAdminView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project_admin.html'


class AnnotationAPIView(View):

    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        once_active_learned = len(Annotation.objects.all().exclude(prob=None)) > 0
        if once_active_learned:
            # Use Annotation model & RawData model.
            # Left outer join data and annotation.
            # Filter manual=False
            # Sort prob
            docs = Annotation.objects.all()
        else:
            # Left outer join data and annotation.
            docs = Document.objects.filter(annotation__isnull=True, project=project)
            docs = [{**d.as_dict(), **{'labels': []}} for d in docs]

        if not docs:
            docs = [{'id': None, 'labels': [], 'text': ''}]

        return JsonResponse({'data': docs})

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        data_id, label_id = body.get('id'), body.get('label_id')  # {id:0, label_id:1}

        data = Document.objects.get(id=data_id)
        label = Label.objects.get(id=label_id)
        Annotation(data=data, label=label, manual=True).save()

        return JsonResponse({})

    def delete(self, request, *args, **kwargs):
        body = json.loads(request.body)
        data_id, label_id = body.get('id'), body.get('label_id')  # {id:0, label_id:1}
        Annotation.objects.get(data=data_id, label=label_id).delete()

        return JsonResponse({})


class SearchAPI(View):

    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        keyword = request.GET.get('keyword')
        docs = Document.objects.filter(project=project_id, text__contains=keyword)
        labels = [[a.as_dict() for a in Annotation.objects.filter(data=d.id)] for d in docs]
        docs = [{**d.as_dict(), **{'labels': []}} for d in docs]
        if not docs:
            docs = [{'id': None, 'labels': [], 'text': ''}]
        # Annotation.objects.select_related('data').all().filter(data__text__contains=keyword)
        paginator = Paginator(docs, 5)
        page = request.GET.get('page', 1)
        page = paginator.get_page(page)
        docs = page.object_list

        return JsonResponse({'data': docs,
                             'has_next': page.has_next(),
                             'has_previous': page.has_previous(),
                             'previous_page_number': page.previous_page_number() if page.has_previous() else None,
                             'next_page_number': page.next_page_number() if page.has_next() else None})


class RawDataAPI(View):

    def get(self, request, *args, **kwargs):
        """Get raw data."""
        data = []
        return JsonResponse({'data': data})

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
        remaining = docs.filter(labels__isnull=True).count()
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
    serializer_class = DocumentSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('text', )

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        queryset = self.queryset.filter(project=project_id)

        return queryset


class AnnotationsAPI(generics.ListCreateAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    pagination_class = None

    def get_queryset(self):
        doc_id = self.kwargs['doc_id']
        queryset = self.queryset.filter(data=doc_id)
        return queryset

    def post(self, request, *args, **kwargs):
        doc_id = self.kwargs['doc_id']
        label_id = request.data['label_id']
        doc = Document.objects.get(id=doc_id)
        label = Label.objects.get(id=label_id)
        annotation = Annotation(data=doc, label=label, manual=True)
        annotation.save()

        return Response(annotation)


class AnnotationAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer

    def get_queryset(self):
        doc_id = self.kwargs['doc_id']
        queryset = self.queryset.filter(data=doc_id)

        return queryset

    def get_object(self):
        annotation_id = self.kwargs['annotation_id']
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=annotation_id)
        self.check_object_permissions(self.request, obj)

        return obj
