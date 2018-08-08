import csv
from io import TextIOWrapper

from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .permissions import SuperUserMixin
from .forms import ProjectForm
from .models import Document, Project


class IndexView(TemplateView):
    template_name = 'index.html'


class ProjectView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return [project.get_template_name()]


class ProjectsView(LoginRequiredMixin, TemplateView):
    model = Project
    paginate_by = 100
    template_name = 'projects.html'

    def get(self, request, *args, **kwargs):
        form = ProjectForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return HttpResponseRedirect(reverse('upload', args=[project.id]))
        else:
            return render(request, self.template_name, {'form': form})


class DatasetView(SuperUserMixin, LoginRequiredMixin, ListView):
    template_name = 'admin/dataset.html'
    paginate_by = 5

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return project.documents.all()


class LabelView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/label.html'


class StatsView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/stats.html'


class DataUpload(SuperUserMixin, LoginRequiredMixin, TemplateView):
    model = Project
    template_name = 'admin/dataset_upload.html'

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        try:
            form_data = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.reader(form_data)
            for line in reader:
                text = line[0]
                Document(text=text, project=project).save()
            return HttpResponseRedirect(reverse('dataset', args=[project.id]))
        except:
            print("failed")
            return HttpResponseRedirect(reverse('dataset-upload', args=[project.id]))


class DataDownload(SuperUserMixin, LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)
        docs = project.get_documents(is_null=False).distinct()
        filename = '_'.join(project.name.lower().split())
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)

        writer = csv.writer(response)
        for d in docs:
            writer.writerows(d.make_dataset())

        return response
