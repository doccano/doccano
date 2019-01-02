import csv
import json
from io import TextIOWrapper

from django.db.utils import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.core import serializers

from .permissions import SuperUserMixin
from .forms import ProjectForm
from .models import Document, Project, SequenceAnnotation, Label
from itertools import cycle

from .colorspace import lightness

COLORSCHEME = ['#a6cee3', '#fb9a99', '#b2df8a', '#fdbf6f', '#cab2d6', '#ffff99',
               '#1f78b4', '#e31a1c', '#33a02c', '#ff7f00', '#6a3d9a', '#b15928']
N_COLORS = (len(COLORSCHEME)//2)

COLORSCHEME_CYCLE = cycle(COLORSCHEME)
TEXT_COLOR_FLAG = True

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

    def unpack_annotation(self, ann):
        try:
            start_offset = ann[self.field_start]
            end_offset = ann[self.field_end]
        except KeyError as ke:
            self.field_start = None
            for alt_s, alt_e in zip(self.field_alt_start, self.field_alt_end):
                if (alt_s in ann) and (alt_e in ann):
                    self.field_start = alt_s
                    self.field_end = alt_e
                    break
            if self.field_start is None:
                raise ke
            start_offset = ann[self.field_start]
            end_offset = ann[self.field_end]
        try:
            label = ann[self.field_label]
        except KeyError as ke:
            self.field_label = None
            for alt_l in self.field_alt_label:
                if (alt_l in ann):
                    self.field_label = alt_l
                    break
            if self.field_label is None:
                raise ke
            label = ann[self.field_label]
        return label, start_offset, end_offset

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        import_format = request.POST['format']
        try:
            if import_format == 'csv':
                form_data = TextIOWrapper(
                    request.FILES['file'].file, encoding='utf-8')
                if project.is_type_of(Project.SEQUENCE_LABELING):
                    Document.objects.bulk_create([
                        Document(text=line.strip(), project=project)
                        for line in form_data
                    ])
                else:
                    reader = csv.reader(form_data)
                    Document.objects.bulk_create([
                        Document(text=line[0].strip(), project=project)
                        for line in reader
                    ])
            elif import_format == 'json':
                # set the annotation dictionary field names.
                # if the pre-set field name is not found, alternatives are assumed
                self.field_alt_start = ['start', 's']
                self.field_alt_end = ['end', 'e']
                self.field_alt_label = ['l', 'id']
                self.field_title = 'title'
                self.field_start = 'start_offset'
                self.field_end = 'end_offset'
                self.field_label = 'label'
                form_data = request.FILES['file'].file
                text_list = json.loads(form_data.read())
                text_list = filter(lambda x: 'text' in x and x['text'] is not None,
                                    text_list)
                docs = []
                seqanns = []
                for entry in text_list:
                    try:
                        title = entry[self.field_title]
                    except:
                        if 'id' in entry:
                            self.field_title='id'
                            title = entry[self.field_title]
                        else:
                            continue
                    doc = Document(text=entry['text'], project=project, title=title)
                    if 'seq_annotations' in entry:
                        # parse annotations    
                        # insert a document
                        doc.save()
                        doc_annotations = entry['seq_annotations']
                        for ann in doc_annotations:
                            lbl, start_, end_ = self.unpack_annotation(ann)
                            try:
                                label = Label.objects.get(
                                              project=project,
                                              text=lbl,
                                              )
                            except Label.DoesNotExist:
                                color = next(COLORSCHEME_CYCLE)
                                text_color='#ffffff' if  lightness(color)<127 \
                                            else '#000000'
                                try:
                                    label = Label(
                                                  project=project,
                                                  text=lbl,
                                                  shortcut=lbl[0],
                                                  background_color=color,
                                                  text_color=text_color,
                                                  )
                                    label.save()
                                except IntegrityError as ei:
                                    labels = Label.objects.filter(project=project)
                                    shortcuts = [la.shortcut for la in labels]
                                    other_lbl = [la.text for la in labels if la.shortcut==lbl[0]][0]
                                    shortcut_proposal = [l1 for l1, l2 in zip(lbl,other_lbl) if l1!=l2]
                                    shortcut_proposal = [x for x in shortcut_proposal if x not in shortcuts]
                                    vowels = set('aeiou')
                                    shortcut_proposal_consonant = [x for x in shortcut_proposal\
                                            if x not in vowels]
                                    if len(shortcut_proposal_consonant)>0:
                                        shortcut = shortcut_proposal_consonant[0]
                                    else:
                                        shortcut = shortcut_proposal[0]
                                    label = Label(
                                                  project=project,
                                                  text=lbl,
                                                  shortcut=shortcut,
                                                  background_color=color,
                                                  text_color=text_color,
                                                  )
                                    label.save()

                            seqann = SequenceAnnotation(
                                            user=request.user,
                                            document=doc,
                                            label=label,
                                            start_offset=start_,
                                            end_offset=end_,
                                            manual=False,
                                            )
                            seqanns.append(seqann)
                    else:
                        docs.append(doc)
                if len(docs)>0:
                    Document.objects.bulk_create(docs)
                if len(seqanns)>0:
                    SequenceAnnotation.objects.bulk_create(seqanns)

            return HttpResponseRedirect(reverse('dataset', args=[project.id]))
        except Exception as ee:
            print("ENTRY", entry)
            print("EXCEPTION", ee)
            return HttpResponseRedirect(reverse('upload', args=[project.id]))


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


class JsonDownload(SuperUserMixin, LoginRequiredMixin, View):
    '''Download annotations as a json file'''
    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)

        filename = '_'.join(project.name.lower().split())
        response = HttpResponse(content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="{}.json"'.format(filename)
        labels = project.labels.all().values()
        labels = {x['id']:x['text'] for x in labels}
        docs = project.get_documents(is_null=False).distinct()
        dump = []
        for doc in docs:
            anns = list(doc.get_annotations().values())
            doc_ = model_to_dict(doc)
            for ann in anns:
                ann.pop('id')
                ann.pop('document_id')
                ann['label'] = labels[ann.pop('label_id')]
            doc_['seq_annotations'] = anns
            dump.append(doc_)

        dump = json.dumps(dump)
        response.write(dump)
        return response

class DemoTextClassification(TemplateView):
    template_name = 'demo/demo_text_classification.html'


class DemoNamedEntityRecognition(TemplateView):
    template_name = 'demo/demo_named_entity.html'


class DemoTranslation(TemplateView):
    template_name = 'demo/demo_translation.html'
