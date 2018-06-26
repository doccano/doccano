import json

import django_filters
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from rest_framework import viewsets, filters

from .models import Annotation, Label, Document, Project
from .serializers import LabelSerializer, ProjectSerializer, DocumentSerializer


class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class InboxView(View):
    template_name = 'annotation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


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


class ProgressAPI(View):

    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        docs = Document.objects.filter(project=project)
        total = docs.count()
        remaining = docs.filter(annotations__isnull=True).count()

        return JsonResponse({'total': total, 'remaining': remaining})


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


class LabelAPI(View):

    def get(self, request, *args, **kwargs):
        """Get labels."""
        project_id = kwargs.get('pk')
        labels = Label.objects.filter(project=project_id)
        labels = [label.as_dict() for label in labels]

        return JsonResponse({'labels': labels})

    def post(self, request, *args, **kwargs):
        """Create labels."""
        #text = request.POST.get('text')
        #shortcut = request.POST.get('shortcut')
        project_id = kwargs.get('pk')
        project = Project.objects.get(id=project_id)
        body = request.body.decode('utf-8').replace("'", '"')
        body = json.loads(body)
        text = body.get('text')
        shortcut = body.get('shortcut')
        label = Label(text=text, shortcut=shortcut, project=project)
        label.save()

        return JsonResponse(label.as_dict())

    def put(self, request, *args, **kwargs):
        """Update labels."""
        body = request.body.decode('utf-8').replace("'", '"')
        body = json.loads(body)
        label_id = body.get('id')
        text = body.get('text')
        shortcut = body.get('shortcut')
        label = Label.objects.get(id=label_id)
        label.text = text
        label.shortcut = shortcut
        label.save()

        return JsonResponse({'status': 'ok'})

    def delete(self, request, *args, **kwargs):
        body = request.body.decode('utf-8').replace("'", '"')
        body = json.loads(body)
        label_id = body.get('id')
        Label.objects.get(id=label_id).delete()

        return JsonResponse({'status': 'ok'})


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


class ProjectListView(ListView):

    model = Project
    paginate_by = 100  # if pagination is desired
    template_name = 'project_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProjectAdminView(DetailView):

    model = Project
    template_name = 'project_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DataDownloadAPI(View):

    def get(self, request, *args, **kwargs):
        annotated_docs = [a.as_dict() for a in Annotation.objects.filter(manual=True)]
        json_str = json.dumps(annotated_docs)
        response = HttpResponse(json_str, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=annotation_data.json'

        return response


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    filter_fields = ('text', 'project')


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
