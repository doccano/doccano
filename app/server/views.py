import csv
import json
from io import TextIOWrapper, StringIO
import itertools as it
import logging
import datetime
import pandas as pd

from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import connection

from django.contrib.auth.forms import UserCreationForm

from .resources import DocumentResource, DocumentAnnotationResource, LabelResource

from .permissions import SuperUserMixin
from .forms import ProjectForm
from .models import Document, Project, DocumentAnnotation, Label, DocumentGoldAnnotation, User
from app import settings
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'


class ProjectView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        if not self.request.user.is_superuser:
            try:
                user = project.users.get(id=self.request.user.id)
            except ObjectDoesNotExist:
                return '404.html'
        return [project.get_template_name()]

    def get_context_data(self, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context = super().get_context_data(**kwargs)
        context['docs_count'] = project.get_docs_count()
        context['project'] = project
        return context


class ProjectsView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'projects.html'


class UsersAdminView(SuperUserMixin, LoginRequiredMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'users.html'

    def form_invalid(self, form):
        print('invalid', form.errors)
        response = super().form_invalid(form)
        return response



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


class UserView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        context = super().get_context_data(**kwargs)
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

class UserInfoView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/user_info.html'

    def get_context_data(self, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context = super().get_context_data(**kwargs)
        context['docs_count'] = project.get_docs_count()
        cursor = connection.cursor()
        annots_sql = '''SELECT server_documentannotation.document_id,
            server_documentannotation.label_id,
            server_documentannotation.user_id,
            server_documentannotation.created_date_time,
            server_documentannotation.updated_date_time
            FROM server_documentannotation
            LEFT JOIN server_document ON server_document.id = server_documentannotation.document_id
            WHERE server_document.project_id = %s AND server_documentannotation.user_id = % s''' % (self.kwargs['project_id'], self.kwargs['user_id'])
        cursor.execute(annots_sql)
        annots_csv = 'user_id,created_date_time,updated_date_time\n'
        for row in cursor.fetchall():
            annots_csv += '%s,%s,%s\n' % (row[2], row[3], row[4])
        pandas_csv = StringIO(annots_csv)
        df = pd.read_csv(pandas_csv, parse_dates=['created_date_time', 'updated_date_time'])
        df = df.sort_values(['user_id', 'created_date_time'])
        users_sessions = pd.DataFrame()
        users_speed = {}
        TH_TIMEOUT_SESSION = 15
        for user_id in df['user_id'].unique():
            d = df[df['user_id'] == user_id]
            d['session'] = d['created_date_time'] - d['created_date_time'].shift()
            d['session'] = (d['session'] > datetime.timedelta(minutes=TH_TIMEOUT_SESSION)).cumsum()
            single_user_sessions = d.groupby('session')['created_date_time'].agg([('count', lambda x: len(x) - 1),
                                                                    ('start_datetime', lambda x: x.iloc[0]),
                                                                    ('end_datetime', lambda x: x.iloc[-1]),
                                                                    ('timediff', lambda x: x.iloc[-1] - x.iloc[0])
                                                        ])
            single_user_sessions['user_id'] = user_id
            users_speed[user_id] = sum(single_user_sessions['timediff'].dt.seconds) / sum(single_user_sessions['count'].astype(int))
            users_sessions = pd.concat([users_sessions, single_user_sessions])
        context['user_speed'] = users_speed[self.kwargs['user_id']]

        user_query = ''' 
        WITH da as (
            SELECT MAX(server_documentannotation.updated_date_time) as last_annotation FROM server_documentannotation WHERE server_documentannotation.user_id = %s
        ),
        ut as(SELECT email, id, username FROM auth_user WHERE auth_user.id = %s),
        pt as(
            SELECT server_project.name as project_name, server_project.id as project_id
            FROM server_project
            INNER JOIN server_project_users
            ON server_project_users.project_id = server_project.id
            WHERE server_project_users.user_id = %s
        )

        SELECT ut.id, ut.email, ut.username, da.last_annotation,  pt.project_id, pt.project_name FROM da, ut, pt
        '''  % (self.kwargs['user_id'], self.kwargs['user_id'], self.kwargs['user_id'])

        cursor.execute(user_query)
        rows = cursor.fetchall()
        context['user_id'] = rows[0][0]
        context['user_email'] = rows[0][1]
        context['user_name'] = rows[0][2]
        context['last_annotation'] = rows[0][3]

        projects = []
        for row in rows:
            projects.append({'id': row[4],'name': row[5]})
        context['projects'] = projects
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
                if row[text_col]=='':
                    continue
                label_obj = Label.objects.filter(text__exact=row[label_col], project=project)
                if len(label_obj)>1:
                    errors.append('Found multiple labels with text "{}"'.format(row[label_col]))
                    continue
                else:
                    label_obj = label_obj.first()

                document_obj = Document.objects.filter(text__exact=row[text_col], project=project)
                if len(document_obj) > 1:
                    errors.append('Found multiple documents with text "{}"'.format(row[text_col]))
                    continue
                else:
                    document_obj = document_obj.first()

                if (label_obj and document_obj):
                    labels_set.append([label_obj, document_obj])
                else:
                    if (not label_obj):
                        errors.append('Label "' + row[label_col] + '" is not found')
                    if (not document_obj):
                        errors.append('Document with text "' + row[text_col] + '" is not found')
            if len(errors):
                raise DataUpload.ImportFileError('Encoutered {} errors: \n\n{}'.format(len(errors), '\n\n'.join(errors)) )

            return (
                DocumentGoldAnnotation(
                    label=label[0],
                    document=label[1]
                )
                for label in labels_set
            )
        else:
            return []

    def users_labeled_csv_to_labels(self, project, file, text_key='text', label_key='label', user_key='user'):
        form_data = TextIOWrapper(file, encoding='utf-8', errors='ignore')
        reader = csv.reader(form_data, quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL, skipinitialspace=True)

        maybe_header = next(reader)
        if maybe_header:
            if (text_key in maybe_header and label_key in maybe_header and user_key in maybe_header):
                text_col = maybe_header.index(text_key)
                label_col = maybe_header.index(label_key)
                user_col = maybe_header.index(user_key)
            elif len(maybe_header) == 3:
                reader = it.chain([maybe_header], reader)
                text_col = 0
                label_col = 1
                user_col = 2
            else:
                raise DataUpload.ImportFileError("CSV file must have either a title with \"text\" column and \"label\" column and \"user\" column or have three columns ")
            errors = []
            labels_set = []
            count = 0
            for row in reader:
                if row[text_col]=='':
                    continue
                label_obj = Label.objects.filter(text__exact=row[label_col], project=project)
                if len(label_obj)>1:
                    errors.append('Found multiple labels with text "{}"'.format(row[label_col]))
                    continue
                else:
                    label_obj = label_obj.first()

                document_obj = Document.objects.filter(text__exact=row[text_col], project=project)
                if len(document_obj) > 1:
                    errors.append('Found multiple documents with text "{}"'.format(row[text_col]))
                    continue
                else:
                    document_obj = document_obj.first()

                user_obj = User.objects.filter(username__exact=row[user_col])

                if len(user_obj) > 1:
                    errors.append('Found multiple users with name "{}"'.format(row[user_col]))
                    continue
                else:
                    user_obj = user_obj.first()

                if (label_obj and document_obj and user_obj):
                    labels_set.append([label_obj, document_obj, user_obj])
                else:
                    if (not label_obj):
                        errors.append('Label "' + row[label_col] + '" is not found')
                    if (not document_obj):
                        errors.append('Document with text "' + row[text_col] + '" is not found')
                    if (not user_obj):
                        errors.append('User with name "' + row[user_col] + '" is not found')
            if len(errors):
                raise DataUpload.ImportFileError('Encoutered {} errors: \n\n{}'.format(len(errors), '\n\n'.join(errors)) )

            return (
                DocumentAnnotation(
                    label=label[0],
                    document=label[1],
                    user=label[2]
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
            users_lsbels = []
            if import_format == 'csv':
                documents = self.csv_to_documents(project, file)
            elif import_format == 'json':
                documents = self.json_to_documents(project, file)
            elif import_format == 'csv_labeled':
                true_labels = self.labeled_csv_to_labels(project, file)
            elif import_format == "csv_labeled_users":
                users_lsbels = self.users_labeled_csv_to_labels(project, file)

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
            elif (import_format == "csv_labeled_users"):
                labels_len = 0
                while True:
                    batch = list(it.islice(users_lsbels, batch_size))
                    if not batch:
                        break
                    labels_len += len(batch)
                    DocumentAnnotation.objects.bulk_create(batch, batch_size=batch_size)
                url = reverse('dataset', args=[project.id])
                url += '?users_labels_count=' + str(labels_len)
                

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

class LabelsAdminDownloadFile(SuperUserMixin, LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        p = get_object_or_404(Project, pk=self.kwargs['project_id'])

        query = '''SELECT server_documentannotation.document_id,
                server_documentannotation.label_id,
                COUNT(DISTINCT user_id) AS num_labelers,
                MAX(server_documentannotation.created_date_time) AS last_annotation_date,
                substr(server_document.text, 0, 60) AS document_text,
				server_documentgoldannotation.label_id as ground_truth,
				server_documentmlmannotation.prob as model_confidence
            FROM server_documentannotation
            LEFT JOIN server_document ON server_document.id = server_documentannotation.document_id
			LEFT JOIN server_documentgoldannotation ON server_documentgoldannotation.document_id = server_documentannotation.document_id
			LEFT JOIN server_documentmlmannotation ON server_documentmlmannotation.document_id = server_documentannotation.document_id
            LEFT JOIN auth_user ON auth_user.id = server_documentannotation.user_id
            WHERE server_document.project_id = %d
            GROUP BY server_documentannotation.document_id, server_documentannotation.label_id, server_document.text, server_documentgoldannotation.label_id, server_documentmlmannotation.prob''' % (self.kwargs['project_id'])
        cursor = connection.cursor()
        cursor.execute(query)
        labels_csv = 'document_id,label_id,ground_truth,model_confidence,num_labelers,last_annotation_date,snippet\n'
        for row in cursor.fetchall():
            labels_csv += '%s,%s,%s,%s,%s,%s,"%s"\n' % (row[0], row[1], row[5], row[6], row[2], row[3], row[4])
        pandas_csv = StringIO(labels_csv)
        df = pd.read_csv(pandas_csv)
        z = df.sort_values(['document_id', 'num_labelers'], ascending=[True, False])\
            .groupby(['document_id'])\
            .agg({
                'label_id': [('top_label', lambda x: x.iloc[0])],
                'num_labelers': [
                    ('agreement', lambda x: round( x.iloc[0] / sum(x)) ),
                    ('num_labelers', lambda x: sum(x)),
                ],
                'last_annotation_date': [
                    ('last_annotation_date', lambda x: x.max())
                ],
                'snippet': [('snippet', lambda x: x.iloc[0])],
                'ground_truth': [('ground_truth', lambda x: x.iloc[0])],
                'model_confidence': [('model_confidence', lambda x: x.iloc[0])],
        })

        z.columns = [c[1] for c in z.columns]
        data = z.reset_index()
        spl = p.name.lower().split()
        spl.append('labels')

        filename = '_'.join(spl)
        try:
            response = self.get_csv(filename, data)
            return response
        except Exception as e:
            logger.exception(e)
            messages.add_message(request, messages.ERROR, "Something went wrong")
            return HttpResponseRedirect(reverse('labels_admin', args=[project.id]))

    def get_csv(self, filename, data):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
        response.write(data.to_csv())
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
