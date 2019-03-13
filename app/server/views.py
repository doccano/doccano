import csv
import json
from io import TextIOWrapper
import itertools as it
import logging

from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .resources import DocumentResource, DocumentAnnotationResource, LabelResource

from .permissions import SuperUserMixin
from .forms import ProjectForm
from .models import Document, Project, DocumentAnnotation, Label, DocumentGoldAnnotation
from app import settings

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'


class ProjectView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return [project.get_template_name()]

    def get_context_data(self, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context = super().get_context_data(**kwargs)
        context['docs_count'] = project.get_docs_count()
        return context


class ProjectsView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'projects.html'


class DatasetView(SuperUserMixin, LoginRequiredMixin, ListView):
    template_name = 'admin/dataset.html'
    paginate_by = 5

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return project.documents.all()

    def get_context_data(self, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context = super().get_context_data(**kwargs)
        context['docs_count'] = project.get_docs_count()
        return context


class LabelView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/label.html'

    def get_context_data(self, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context = super().get_context_data(**kwargs)
        context['docs_count'] = project.get_docs_count()
        return context


class LabelersView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/labelers.html'

    def get_context_data(self, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context = super().get_context_data(**kwargs)
        context['docs_count'] = project.get_docs_count()
        return context


class LabelAdminView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/labels_admin.html'

    def get_context_data(self, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context = super().get_context_data(**kwargs)
        context['docs_count'] = project.get_docs_count()
        return context

class StatsView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/stats.html'

    def get_context_data(self, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context = super().get_context_data(**kwargs)
        context['docs_count'] = project.get_docs_count()
        return context


class GuidelineView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/guideline.html'

    def get_context_data(self, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context = super().get_context_data(**kwargs)
        context['docs_count'] = project.get_docs_count()
        return context

class SettingsView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context = super().get_context_data(**kwargs)
        context['project'] = project
        context['docs_count'] = project.get_docs_count()
        return context


class DataUpload(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/dataset_upload.html'

    class ImportFileError(Exception):
        def __init__(self, message):
            self.message = message

    def extract_metadata_csv(self, row, text_col, header_without_text):
        vals_without_text = [val for i, val in enumerate(row) if i != text_col]
        return json.dumps(dict(zip(header_without_text, vals_without_text)))

    def csv_to_documents(self, project, file, text_key='text'):
        form_data = TextIOWrapper(file, encoding='utf-8', errors='ignore')
        reader = csv.reader(form_data)

        maybe_header = next(reader)
        if maybe_header:
            if text_key in maybe_header:
                text_col = maybe_header.index(text_key)
            elif len(maybe_header) == 1:
                reader = it.chain([maybe_header], reader)
                text_col = 0
            else:
                raise DataUpload.ImportFileError("CSV file must have either a title with \"text\" column or have only one column ")

            header_without_text = [title for i, title in enumerate(maybe_header)
                                   if i != text_col]
            fixed_utf = []

            return (
                Document(
                    text=row[text_col],
                    metadata=self.extract_metadata_csv(row, text_col, header_without_text),
                    project=project
                )
                for row in reader
                if row!=[] and row!=''
            )
        else:
            return []

    def labeled_csv_to_labels(self, project, file, text_key='text', label_key='label'):
        form_data = TextIOWrapper(file, encoding='utf-8', errors='ignore')
        reader = csv.reader(form_data, quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL, skipinitialspace=True)

        maybe_header = next(reader)
        if maybe_header:
            if (text_key in maybe_header and label_key in maybe_header):
                text_col = maybe_header.index(text_key)
                label_col = maybe_header.index(label_key)
            elif len(maybe_header) == 2:
                reader = it.chain([maybe_header], reader)
                text_col = 0
                label_col = 1
            else:
                raise DataUpload.ImportFileError("CSV file must have either a title with \"text\" column and \"label\" column or have two columns ")
            errors = []
            labels_set = []
            count = 0
            for row in reader:
                label_obj = Label.objects.filter(text__exact=row[label_col]).first()
                document_obj = Document.objects.filter(text__exact=row[text_col]).first()
                if (label_obj and document_obj):
                    labels_set.append([label_obj, document_obj])
                else:
                    if (not label_obj):
                        errors.append('Label "' + row[label_col] + '" is not found')
                    if (not document_obj):
                        errors.append('Document with text "' + row[text_col] + '" is not found')
                    raise DataUpload.ImportFileError('\n'.join(errors))

            return (
                DocumentGoldAnnotation(
                    label=label[0],
                    document=label[1]
                )
                for label in labels_set
            )
        else:
            return []

    def extract_metadata_json(self, entry, text_key):
        copy = entry.copy()
        del copy[text_key]
        return json.dumps(copy)

    def json_to_documents(self, project, file, text_key='text'):
        parsed_entries = (json.loads(line) for line in file)

        return (
            Document(text=entry[text_key], metadata=self.extract_metadata_json(entry, text_key), project=project)
            for entry in parsed_entries
        )

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        import_format = request.POST['format']
        try:
            file = request.FILES['file'].file
            documents = []
            true_labels = []
            if import_format == 'csv':
                documents = self.csv_to_documents(project, file)
            elif import_format == 'json':
                documents = self.json_to_documents(project, file)
            elif import_format == 'csv_labeled':
                true_labels = self.labeled_csv_to_labels(project, file)

            batch_size = settings.IMPORT_BATCH_SIZE

            if (import_format == 'csv' or import_format == 'json'):
                docs_len = 0
                while True:
                    batch = list(it.islice(documents, batch_size))
                    if not batch:
                        break
                    docs_len += len(batch)
                    Document.objects.bulk_create(batch, batch_size=batch_size)
                url = reverse('dataset', args=[project.id])
                url += '?docs_count=' + str(docs_len)
                return HttpResponseRedirect(url)
            elif (import_format == 'csv_labeled'):
                labels_len = 0
                while True:
                    batch = list(it.islice(true_labels, batch_size))
                    if not batch:
                        break
                    labels_len += len(batch)
                    DocumentGoldAnnotation.objects.bulk_create(batch, batch_size=batch_size)
                url = reverse('dataset', args=[project.id])
                url += '?true_labels_count=' + str(labels_len)
                return HttpResponseRedirect(url)
        except DataUpload.ImportFileError as e:
            messages.add_message(request, messages.ERROR, e.message)
            return HttpResponseRedirect(reverse('upload', args=[project.id]))
        except Exception as e:
            logger.exception(e)
            messages.add_message(request, messages.ERROR, 'Something went wrong')
            messages.add_message(request, messages.ERROR, e)
            return HttpResponseRedirect(reverse('upload', args=[project.id]))
    
    def get_context_data(self, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context = super().get_context_data(**kwargs)
        context['docs_count'] = project.get_docs_count()
        return context


class DataDownload(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/dataset_download.html'

    def get_context_data(self, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context = super().get_context_data(**kwargs)
        context['docs_count'] = project.get_docs_count()
        return context


class DocumentExport(SuperUserMixin, LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        queryset = Document.objects.filter(project=project)
        dataset = DocumentResource().export(queryset)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}_documents.csv"'.format(project)
        response.write(dataset.csv)
        return response

class DocumentAnnotationExport(SuperUserMixin, LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        project_docs = Document.objects.filter(project=project)
        queryset = DocumentAnnotation.objects.filter(document__in=project_docs)
        dataset = DocumentAnnotationResource().export(queryset)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}_annotations.csv"'.format(project)
        response.write(dataset.csv)
        return response

class LabelExport(SuperUserMixin, LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        queryset = Label.objects.filter(project=project)
        dataset = LabelResource().export(queryset)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}_labels.csv"'.format(project)
        response.write(dataset.csv)
        return response

class DataDownloadFile(SuperUserMixin, LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)
        docs = project.get_documents(is_null=False).distinct()
        export_format = request.GET.get('format')
        filename = '_'.join(project.name.lower().split())
        try:
            if export_format == 'csv':
                response = self.get_csv(filename, docs)
            elif export_format == 'json':
                response = self.get_json(filename, docs)
            return response
        except Exception as e:
            logger.exception(e)
            messages.add_message(request, messages.ERROR, "Something went wrong")
            return HttpResponseRedirect(reverse('download', args=[project.id]))

    def get_csv(self, filename, docs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
        writer = csv.writer(response)
        for d in docs:
            writer.writerows(d.to_csv())
        return response

    def get_json(self, filename, docs):
        response = HttpResponse(content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="{}.json"'.format(filename)
        for d in docs:
            dump = json.dumps(d.to_json(), ensure_ascii=False)
            response.write(dump + '\n')  # write each json object end with a newline
        return response


class LoginView(BaseLoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    extra_context = {
        'github_login': bool(settings.SOCIAL_AUTH_GITHUB_KEY),
        'aad_login': bool(settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID),
    }

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['social_login_enabled'] = any(value for key, value in context.items()
                                              if key.endswith('_login'))
        return context


class DemoTextClassification(TemplateView):
    template_name = 'demo/demo_text_classification.html'


class DemoNamedEntityRecognition(TemplateView):
    template_name = 'demo/demo_named_entity.html'


class DemoTranslation(TemplateView):
    template_name = 'demo/demo_translation.html'
