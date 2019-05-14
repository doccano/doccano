import csv
import os
import operator
# import gensim.downloader as api

from random import randint
import datetime

import json

from collections import Counter
from itertools import chain
from itertools import islice

import matplotlib.pyplot as plt
import seaborn as sns
import base64

import pandas as pd
import numpy as np
import scipy as sp
from io import StringIO, BytesIO

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.db.models import Case, When
from django.db import connection
from django.db.models.expressions import RawSQL
from rest_framework import viewsets, generics, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project, Label, Document, DocumentAnnotation, DocumentMLMAnnotation
from .permissions import IsAdminUserAndWriteOnly, IsProjectUser, IsOwnAnnotation
from .serializers import ProjectSerializer, LabelSerializer, Word2vecSerializer
from .filters import ExcludeSearchFilter

from .labelers_comparison_functions import create_kappa_comparison_df, rank_labelers, add_agreement_columns


from classifier.text.text_classifier import run_model_on_file

ML_FOLDER = 'ml_models'

OUTPUT_FILE = 'ml_out.csv'
INPUT_FILE = 'ml_input.csv'


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, IsAdminUserAndWriteOnly)

    def get_queryset(self):
        queryset = self.request.user.projects
        return queryset

    @action(methods=['get'], detail=True)
    def progress(self, request, pk=None):
        project = self.get_object()
        return Response(project.get_progress(self.request.user))


class LabelList(generics.ListCreateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get_queryset(self):
        queryset = self.queryset.filter(project=self.kwargs['project_id'])

        return queryset

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        serializer.save(project=project)

class LabelersListAPI(APIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)
    def render_agreement_matrix(self):
        return 'data:image/gif;base64,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'
    
    def get_truth_agreement(self):
        cursor = connection.cursor()

        return 42

    def get_labelers_agreement(self):
        return 42

    def get(self, request, *args, **kwargs):
        p = get_object_or_404(Project, pk=self.kwargs['project_id'])
        users = []
        cursor = connection.cursor()

        agreement_csv = 'user_id,document_id,label_id,true_label_id\n'

        users_agreement_query = '''SELECT
            server_documentannotation.user_id,
            server_documentannotation.document_id,
            server_documentannotation.label_id
            FROM auth_user
            LEFT JOIN server_documentannotation ON auth_user.id = server_documentannotation.user_id
            LEFT JOIN server_document ON server_documentannotation.document_id = server_document.id
            WHERE server_document.project_id = ''' + str(self.kwargs['project_id'])
        cursor.execute(users_agreement_query)
        agreement_array = []
        for row in cursor.fetchall():
            agreement_array.append([row[0], row[1], row[2]])
            #agreement_csv += '%s,%s,%s\n' % (row[0], row[1], row[2])

        gold_labels_query = '''SELECT
            server_documentgoldannotation.document_id,
            server_documentgoldannotation.label_id
            FROM server_documentgoldannotation
            LEFT JOIN server_document ON server_documentgoldannotation.document_id = server_document.id
            WHERE server_document.project_id = ''' + str(self.kwargs['project_id'])
        cursor.execute(gold_labels_query)
        for row in cursor.fetchall():
            for ar in agreement_array:
                if (ar[1] == row[0]):
                    ar.append(row[1])
        for row in agreement_array:
            if len(row) > 3:
                agreement_csv += '%s,%s,%s,%s\n' % (row[0], row[1], row[2], row[3])
            else:
                agreement_csv += '%s,%s,%s\n' % (row[0], row[1], row[2])
        pandas_csv = StringIO(agreement_csv)

        df = pd.read_csv(pandas_csv)
        df.to_csv('temp_agreement.csv')
        df = df.drop_duplicates(['document_id', 'user_id'])
        pivot_table = df.pivot(index='document_id', columns='user_id', values='label_id')
        agreement = create_kappa_comparison_df(pivot_table)

        users_agreement = rank_labelers(agreement)

        users_query = '''WITH da AS (
            SELECT COUNT(DISTINCT server_documentannotation.document_id) as num_documents_reviewed,
                MAX(server_documentannotation.updated_date_time) as last_annotation,
                COUNT(server_documentannotation.id) AS num_annotations,
                server_documentannotation.user_id as user_id
            FROM server_documentannotation INNER JOIN server_document ON server_documentannotation.document_id = server_document.id
            WHERE server_document.project_id = %d
            GROUP BY server_documentannotation.user_id
            )
            SELECT
            da.user_id,
            auth_user.email,
            auth_user.username,
            auth_user.first_name,
            auth_user.last_name,
            auth_user.last_login,
            da.last_annotation,
            da.num_documents_reviewed,
            da.num_annotations
            FROM
            auth_user
            INNER JOIN da ON auth_user.id = da.user_id''' % (self.kwargs['project_id'])
        cursor.execute(users_query)
        users = []

        for row in cursor.fetchall():
            users.append({
                'id': row[0],
                'name': row[2],
                'count': row[8],
                'last_date': row[6],
                'truth_agreement': self.get_truth_agreement()
            })

        sns_plot = sns.heatmap(agreement, annot=True)
        fig = sns_plot.get_figure()
        fig_bytes = BytesIO()
        fig.savefig(fig_bytes, format='png')
        fig_bytes.seek(0)
        base64b = base64.b64encode(fig_bytes.read())
        fig_bytes.close()
        plt.clf()

        #agreement_truth = add_agreement_columns(pivot_table, 'true_label_id')

        #print(agreement_truth)

        response = {'users': users, 'matrix': base64b, 'users_agreement': users_agreement.fillna(1).to_dict()}
        return Response(response)

class LabelAdminAPI(APIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

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
        z = z.reset_index()
        response = {'dataframe': z}
        return Response(response)

class UserInfo(APIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)
    def get(self, request, *args, **kwargs):
        return Response({})

class RunModelAPI(APIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        p = get_object_or_404(Project, pk=project_id)
        cursor = connection.cursor()

        doc_annotations_query = '''SELECT
            server_document.id,
            server_document.text,
            server_documentannotation.label_id
            FROM
            server_document
            LEFT JOIN server_documentannotation ON server_documentannotation.document_id = server_document.id AND server_documentannotation.user_id = %s
            WHERE server_document.project_id = %s''' % (str(request.user.id), str(self.kwargs['project_id']))

        doc_annotations_gold_query = '''SELECT
            server_document.id,
            server_document.text,
            server_documentgoldannotation.label_id
            FROM
            server_document
            LEFT JOIN server_documentgoldannotation ON server_documentgoldannotation.document_id = server_document.id
            WHERE server_document.project_id =''' + str(self.kwargs['project_id'])

        if not os.path.isdir(ML_FOLDER):
            os.makedirs(ML_FOLDER)
        with open(os.path.join(ML_FOLDER, INPUT_FILE), 'w', encoding='utf-8', newline='') as outfile:
            wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
            wr.writerow(['document_id', 'text', 'label_id'])
            cursor.execute(doc_annotations_query)
            for row in cursor.fetchall():
                label_id = None
                wr.writerow([row[0], row[1], row[2]])

        result = run_model_on_file(os.path.join(ML_FOLDER, INPUT_FILE), os.path.join(ML_FOLDER, OUTPUT_FILE), user_id=0, project_id=project_id)

        reader = csv.DictReader(open(os.path.join(ML_FOLDER, OUTPUT_FILE), 'r', encoding='utf-8'))
        DocumentMLMAnnotation.objects.all().delete()

        batch_size = 1000
        new_annotations = (DocumentMLMAnnotation(document=Document.objects.get(pk=row['document_id']), label=Label.objects.get(pk=int(float(row['label_id']))), prob=row['prob']) for row in reader)
        while True:
            batch = list(islice(new_annotations, batch_size))
            if not batch:
                break
            DocumentMLMAnnotation.objects.bulk_create(batch, batch_size)
        # os.remove(INPUT_FILE)
        # os.remove(OUTPUT_FILE)
        return Response({'result': '<pre>'+result+'</pre>'})

class ProjectStatsAPI(APIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get(self, request, *args, **kwargs):
        p = get_object_or_404(Project, pk=self.kwargs['project_id'])
        labels = [label.text for label in p.labels.all()]
        users = [user.username for user in p.users.all()]
        docs = [doc for doc in p.documents.all()]
        nested_labels = [[a.label.text for a in doc.get_annotations()] for doc in docs]
        nested_users = [[a.user.username for a in doc.get_annotations()] for doc in docs]

        label_count = Counter(chain(*nested_labels))
        label_data = [label_count[name] for name in labels]

        user_count = Counter(chain(*nested_users))
        user_data = [user_count[name] for name in users]

        response = {'label': {'labels': labels, 'data': label_data},
                    'user': {'users': users, 'data': user_data}}

        return Response(response)

class DocumentExplainAPI(generics.RetrieveUpdateDestroyAPIView):
    project_id = 999 # TODO: Change this to the actual current project
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)
    class_weights = None
    filename = 'ml_models/ml_logistic_regression_weights_{project_id}.csv'.format(project_id=project_id)
    has_weights = False
    if (os.path.isfile(filename)):
        class_weights = pd.read_csv(os.path.abspath(filename), header=None,
                    names=['term', 'weight']).set_index('term')['weight']
        has_weights = True
        
    def get(self, request, *args, **kwargs):
        d = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        doc_text_splited = d.text.split(' ')
        format_str_positive = '<span class="has-background-success">{}</span>'
        format_str_negative = '<span class="has-background-danger">{}</span>'
        text = []
        if self.has_weights:
            for w in doc_text_splited:
                weight = self.class_weights.get(w.lower().replace(',','').replace('.',''), 0)
                if weight < -0.2:
                    text.append(format_str_negative.format(w))
                elif weight > 0.2:
                    text.append(format_str_positive.format(w))
                else:
                    text.append(w)
        response = {'document': ' '.join(text)}
        # doc_text_splited = [w if np.abs(self.class_weights.get(w,0))<0.2 else format_str.format(w) for w in doc_text_splited]
        # doc_text_splited[0] = '<span class="has-background-primary">' + doc_text_splited[0] + '</span>'
        # response = {'document': ' '.join(doc_text_splited)}
        return Response(response)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def get_queryset(self):
        queryset = self.queryset.filter(project=self.kwargs['project_id'])
        return queryset


class LabelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def get_queryset(self):
        queryset = self.queryset.filter(project=self.kwargs['project_id'])

        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['label_id'])
        self.check_object_permissions(self.request, obj)

        return obj


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = project.get_document_serializer()

        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset.filter(project=self.kwargs['project_id'])

        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['doc_id'])
        self.check_object_permissions(self.request, obj)

        return obj

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = LabelSerializer
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def get_queryset(self):
        queryset = self.queryset
        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['user_id'])
        self.check_object_permissions(self.request, obj)

        return obj


class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    filter_backends = (ExcludeSearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('text', )
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = project.get_document_serializer()

        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        queryset = self.queryset

        if self.request.query_params.get('is_checked'):
            is_null = self.request.query_params.get('is_checked') == 'true'
            queryset = project.get_documents(is_null).distinct()

        if (project.use_machine_model_sort):
            queryset = queryset.order_by('doc_mlm_annotations__prob').filter(project=self.kwargs['project_id']).exclude(doc_mlm_annotations__prob__isnull=True)
        else:
            queryset = queryset.order_by('doc_annotations__prob').filter(project=self.kwargs['project_id'])

        if (self.request.query_params.get('rules')):
            result = []
            rules = json.loads(self.request.query_params['rules'])
            if (len(rules) > 0):
                rule = rules[0]
                for doc in Document.objects.all():
                    should_append = False
                    metatext = getattr(doc, 'metadata')
                    metadata = json.loads(metatext)
                    if (metadata.get(rule['field'])):
                        if (rule['comparator'] == 'eq' and metadata[rule['field']] == rule['search']):
                            should_append = True
                        elif (rule['comparator'] == 'leq' and metadata[rule['field']] <= rule['search']):
                            should_append = True
                        elif (rule['comparator'] == 'lt' and metadata[rule['field']] < rule['search']):
                            should_append = True
                        elif (rule['comparator'] == 'geq' and metadata[rule['field']] >= rule['search']):
                            should_append = True
                        elif (rule['comparator'] == 'gt' and metadata[rule['field']] > rule['search']):
                            should_append = True
                    if (should_append):
                        result.append(doc.id)
                queryset = queryset.filter(id__in=result)

        return queryset

class MetadataAPI(APIView):
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get(self, request, *args, **kwargs):
        p = get_object_or_404(Project, pk=self.kwargs['project_id'])

        query = '''SELECT DISTINCT metadata FROM server_document WHERE server_document.project_id = %d''' % (self.kwargs['project_id'])
        cursor = connection.cursor()
        cursor.execute(query)
        metadata = [row[0] for row in cursor.fetchall()]
        # metadata = []
        # for row in cursor.fetchall():
        #     metadata.append(row[0])
        
        response = {'metadata': metadata}
        return Response(response)

class AnnotationList(generics.ListCreateAPIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser)

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = project.get_annotation_serializer()

        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        document = project.documents.get(id=self.kwargs['doc_id'])
        self.queryset = document.get_annotations()
        self.queryset = self.queryset.filter(user=self.request.user)

        return self.queryset

    def perform_create(self, serializer):
        doc = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        serializer.save(document=doc, user=self.request.user)


class AnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsProjectUser, IsOwnAnnotation)

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = project.get_annotation_serializer()

        return self.serializer_class

    def get_queryset(self):
        document = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        self.queryset = document.get_annotations()

        return self.queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['annotation_id'])
        self.check_object_permissions(self.request, obj)

        return obj


class SuggestedTerms(generics.ListAPIView):
    """API endpoint to return suggested terms

    Endpoint is:
    /projects/<:id>/suggested/?word=<word_to_cmpare>
    endpoint should return list of suggested words
    """

    permission_classes = (IsAuthenticated, IsProjectUser)
    # In the load section we can pass both link or filename
    # model = api.load("glove-wiki-gigaword-100")

    class DummyWV:
        def most_similar(self, words_list):
            return [w[::-1] for w in words_list]

    model = DummyWV()
    serializer_class = Word2vecSerializer


    def get_queryset(self):
        w = self.request.GET.get("word", "")
        queryset = self.model.most_similar(positive=[w])
        # print(queryset)
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        response = self.get_object()

        return Response(response)
