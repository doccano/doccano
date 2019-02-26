import csv
import json
from io import TextIOWrapper
import itertools as it
import logging

from django.contrib.auth.views import LoginView as BaseLoginView
from django.db import transaction, utils
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .permissions import SuperUserMixin
from .forms import ProjectForm
from .models import Document, Project, Label, DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation
from app import settings

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'


class ProjectView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return [project.get_template_name()]


class ProjectsView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'projects.html'


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


class GuidelineView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/guideline.html'


class DataUpload(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/dataset_upload.html'
    special_keys = ['doc_id', 'external_id', 'text', 'username', 'metadata', 'entities', 'labels', 'sentences']

    class ImportFileError(Exception):
        def __init__(self, message):
            self.message = message

    @staticmethod
    def get_document_id(entry):
        """
        Determine the ID of a document to insert if the same document already
        exists based on a given internal or external ID.
        If both an internal and external ID are given, the external ID takes
        precedence over the internal ID.

        :param entry: entry to check ID for
        :return: document ID or None if document does not exist and no doc_id was given
        """

        external_id = entry.get('external_id', None)
        if external_id is not None:
            try:
                return Document.objects.get(external_id=external_id).id
            except Document.DoesNotExist:
                # if an external ID exists, we do not want to overwrite any internal IDs
                return None

        return entry.get('doc_id', None)

    def load_csv_file(self, file, ignore_id=False):
        form_data = TextIOWrapper(file, encoding='utf-8')
        reader = csv.reader(form_data)

        maybe_header = next(reader)
        if maybe_header:
            header_map = {i: title for i, title in enumerate(maybe_header)}

            if 'text' not in maybe_header:
                if len(maybe_header) == 1:
                    header_map = {0: 'text'}
                    reader = it.chain([maybe_header], reader)
                else:
                    raise DataUpload.ImportFileError('CSV file must have either a title with "text" column or have only one column ')

            for row in reader:
                doc = {header_map[i]: val for i, val in enumerate(row)}
                if ignore_id and 'doc_id' in doc:
                    del doc['doc_id']
                elif not ignore_id:
                    doc['doc_id'] = self.get_document_id(doc)

                yield doc
        else:
            return []

    def load_json_file(self, file, ignore_id=False):
        for doc in (json.loads(line) for line in file):
            if ignore_id and 'doc_id' in doc:
                del doc['doc_id']
            elif not ignore_id:
                doc['doc_id'] = self.get_document_id(doc)

            yield doc

    def csv_to_documents(self, project, file, special_keys=None, ignore_id=False):
        for doc in self.load_csv_file(file, ignore_id):
            yield Document(id=doc.get('doc_id', None),
                           external_id=doc.get('external_id', None),
                           text=doc.get('text', None),
                           metadata=self.extract_metadata(doc, special_keys),
                           project=project)

    def json_to_documents(self, project, file, special_keys=None, ignore_id=False):
        for doc in self.load_json_file(file, ignore_id):
            yield Document(id=doc.get('doc_id', None),
                           external_id=doc.get('external_id', None),
                           text=doc.get('text', None),
                           metadata=self.extract_metadata(doc, special_keys),
                           project=project)

    def import_csv(self, project, file, special_keys=None, ignore_ids=False, batch_size=None):
        """
        Import documents from CSV to the database as one transaction and update existing
        documents where necessary.

        :param project: project Model
        :param file: input CSV file
        :param special_keys: titles of columns to exclude from meta data
        :param ignore_ids: do not import IDs (i.e. do not update existing, insert new instead)
        :param batch_size: number of documents per batch transaction
        """

        doc_it = self.csv_to_documents(project, file, special_keys, ignore_ids)

        while True:
            batch = list(it.islice(doc_it, batch_size))
            if not batch:
                break

            with transaction.atomic():
                for doc in batch:
                    # Re-import of annotations from CSV is not supported
                    doc.save()

    def import_json(self, project, file, user, special_keys=None, ignore_ids=False, batch_size=None):
        """
        Import documents and annotations from JSON to the database as one transaction and
        update existing documents where necessary.

        :param project: project Model
        :param file: input JSON file
        :param user: user Model to reference in saved annotations
        :param special_keys: titles of fields to exclude from meta data
        :param ignore_ids: do not import IDs (i.e. do not update existing, insert new instead)
        :param batch_size: number of documents per batch transaction
        """

        doc_it = self.load_json_file(file, ignore_id=ignore_ids)
        label_map = {}

        def __get_label(l):
            if l not in label_map:
                label_map[l] = Label.objects.get_or_create(project=project, text=l)[0]
            return label_map[l]

        while True:
            batch = list(it.islice(doc_it, batch_size))
            if not batch:
                break

            with transaction.atomic():
                for source in batch:
                    doc = Document(id=source.get('doc_id'),
                                   external_id=source.get('external_id', None),
                                   text=source.get('text', None),
                                   metadata=self.extract_metadata(source, special_keys),
                                   project=project)
                    doc.save()

                    # Document classification annotations found
                    if project.is_type_of(Project.DOCUMENT_CLASSIFICATION) and 'labels' in source:
                        if type(source['labels']) is not list:
                            raise DataUpload.ImportFileError("JSON error: 'labels' must be a list.")

                        # Delete existing annotations for this document before inserting new ones
                        DocumentAnnotation.objects.filter(document=doc).delete()
                        DocumentAnnotation.objects.bulk_create(
                            (DocumentAnnotation(document=doc, user=user, label=__get_label(label))
                                for label in source['labels']))

                    # Sequence annotations found
                    elif project.is_type_of(Project.SEQUENCE_LABELING) and 'entities' in source:
                        if type(source['entities']) is not list:
                            raise DataUpload.ImportFileError("JSON error: 'entities' must be a list.")

                        SequenceAnnotation.objects.filter(document=doc).delete()
                        try:
                            SequenceAnnotation.objects.bulk_create(
                                (SequenceAnnotation(document=doc,
                                                    user=user,
                                                    start_offset=annotation[0],
                                                    end_offset=annotation[1],
                                                    label=__get_label(annotation[2]))
                                 for annotation in source['entities']))
                        except (TypeError, KeyError, IndexError):
                            raise DataUpload.ImportFileError("JSON error: entities must be triples of (int, int, str).")

                    # Sequence2Sequence annotations found
                    elif project.is_type_of(Project.Seq2seq) and 'sentences' in source:

                        if type(source['sentences']) is not list:
                            raise DataUpload.ImportFileError("JSON error: 'sentences' must be a list.")

                        Seq2seqAnnotation.objects.filter(document=doc).delete()
                        Seq2seqAnnotation.objects.bulk_create((Seq2seqAnnotation(document=doc, user=user, text=sentence)
                                                               for sentence in source['sentences']))

    def extract_metadata(self, entry, special_keys, metadata_key='metadata'):
        copy = entry.copy()
        meta = {}
        if metadata_key in copy and type(copy[metadata_key]) is dict:
            meta = copy[metadata_key].copy()

        if special_keys is None:
            special_keys = self.special_keys

        for key in special_keys:
            if key in copy:
                del copy[key]

        copy.update(meta)
        return json.dumps(copy)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        import_format = request.POST['format']
        ignore_ids = 'update_existing' not in request.POST
        import_annotations = 'import_annotations' in request.POST
        batch_size = settings.IMPORT_BATCH_SIZE

        try:
            file = request.FILES['file'].file
            documents = []

            if not import_annotations:
                if import_format == 'csv':
                    documents = self.csv_to_documents(project, file, ignore_id=ignore_ids)

                elif import_format == 'json':
                    documents = self.json_to_documents(project, file, ignore_id=ignore_ids)

                while True:
                    batch = list(it.islice(documents, batch_size))
                    if not batch:
                        break

                    if ignore_ids:
                        Document.objects.bulk_create(batch, batch_size)
                    else:
                        with transaction.atomic():
                            for doc in batch:
                                doc.save()

            elif import_format == 'csv':
                self.import_csv(project, file, ignore_ids=ignore_ids, batch_size=batch_size)
            elif import_format == 'json':
                self.import_json(project, file, user=request.user, ignore_ids=ignore_ids, batch_size=batch_size)

            return HttpResponseRedirect(reverse('dataset', args=[project.id]))

        except utils.IntegrityError as e:
            if 'UNIQUE' in str(e):
                msg = 'UNIQUE constraint failed. Are you trying to import a duplicate external_id?'
            else:
                msg = str(e)
            messages.add_message(request, messages.ERROR, "Data integrity error: {}".format(msg))
            return HttpResponseRedirect(reverse('upload', args=[project.id]))
        except DataUpload.ImportFileError as e:
            messages.add_message(request, messages.ERROR, e.message)
            return HttpResponseRedirect(reverse('upload', args=[project.id]))
        except Exception as e:
            logger.exception(e)
            messages.add_message(request, messages.ERROR, 'Something went wrong')
            return HttpResponseRedirect(reverse('upload', args=[project.id]))


class DataDownload(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/dataset_download.html'


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
