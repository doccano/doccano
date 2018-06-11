import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Annotation, Label, Document, Project


class AnnotationView(View):
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


class MetaInfoAPI(View):

    def get(self, request, *args, **kwargs):
        total = Document.objects.count()
        remaining = Document.objects.filter(annotation__isnull=True).count()

        return JsonResponse({'total': total, 'remaining': remaining})


class SearchAPI(View):

    def get(self, request, *args, **kwargs):
        keyword = request.GET.get('keyword')
        docs = Document.objects.filter(text__contains=keyword)
        labels = [[a.as_dict() for a in Annotation.objects.filter(data=d.id)] for d in docs]
        # print(annotations)
        # print(docs)
        docs = [{**d.as_dict(), **{'labels': []}} for d in docs]
        # Annotation.objects.select_related('data').all().filter(data__text__contains=keyword)

        return JsonResponse({'data': docs})


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
