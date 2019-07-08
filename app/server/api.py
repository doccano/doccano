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
from .serializers import ProjectSerializer, LabelSerializer, Word2vecSerializer, UserSerializer
from .filters import ExcludeSearchFilter

from .labelers_comparison_functions import create_kappa_comparison_df, compute_average_agreement_per_labeler, add_agreement_columns

from app.settings import ML_FOLDER, INPUT_FILE, OUTPUT_FILE

# from classifier.text.text_classifier import run_model_on_file


def get_labels_admin(project_id):
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
        WHERE server_document.project_id = {project_id}
        GROUP BY server_documentannotation.document_id, 
          server_documentannotation.label_id, 
          server_document.text, 
          server_documentgoldannotation.label_id, 
          server_documentmlmannotation.prob
        ORDER BY  server_documentannotation.document_id ASC,
          num_labelers DESC 
          '''.format(project_id=project_id)

    cursor = connection.cursor()
    cursor.execute(query)
    df = pd.DataFrame(cursor.fetchall(), columns=[
        'document_id', 'label_id', 'num_labelers', 'last_annotation_date', 'snippet', 'ground_truth', 'model_confidence'
    ])
    z = df.sort_values(['document_id', 'num_labelers'], ascending=[True, False]) \
        .groupby(['document_id']) \
        .agg({
        'label_id': [('top_label', lambda x: x.iloc[0])],
        'num_labelers': [
            ('agreement', lambda x: x.iloc[0] / sum(x)),
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
    z['ground_truth'] = z['ground_truth'].fillna(-1)
    return z


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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, IsAdminUserAndWriteOnly)


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

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

class LabelersListAPI(APIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get(self, request, *args, **kwargs):
        # def get_annotations
        # p = get_object_or_404(Project, pk=self.kwargs['project_id'])
        cursor = connection.cursor()
        project_id = self.kwargs['project_id']

        def get_annotations(cursor, project_id):
            annotations_query = '''SELECT
                server_documentannotation.user_id,
                server_documentannotation.document_id,
                server_documentannotation.label_id,
                server_documentgoldannotation.label_id AS truth_label_id
                FROM server_documentannotation 
                -- LEFT JOIN server_documentannotation ON auth_user.id = server_documentannotation.user_id
                LEFT JOIN server_document ON server_documentannotation.document_id = server_document.id
                LEFT JOIN server_documentgoldannotation ON server_documentgoldannotation.document_id = server_document.id
                WHERE server_document.project_id = {project_id}'''.format(project_id=project_id)
            cursor.execute(annotations_query)
            annotations = pd.DataFrame(
                cursor.fetchall(),
                columns=['user_id', 'document_id', 'label_id', 'true_label_id']
            )
            return annotations

        def get_users_data(cursor, project_id):
            users_query = '''
              WITH da AS (
                SELECT 
                    COUNT(DISTINCT server_documentannotation.document_id) as num_documents_reviewed,
                    MAX(server_documentannotation.updated_date_time) as last_annotation,
                    COUNT(server_documentannotation.id) AS num_annotations,
                    server_documentannotation.user_id as user_id
                    
                FROM server_documentannotation 
                INNER JOIN server_document ON server_documentannotation.document_id = server_document.id
                WHERE server_document.project_id = {project_id}
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
                FROM auth_user
                INNER JOIN da ON auth_user.id = da.user_id'''.format(project_id=project_id)
            cursor.execute(users_query)
            users = pd.DataFrame(cursor.fetchall(), columns=[
                'id',
                'email',
                'name',
                'first_name',
                'last_name',
                'last_login',
                'last_annotation',
                'num_documents_reviewed',
                'num_annotations'
            ])
            return users.set_index('id')

        def plot_agreement_matrix(agreement):
            sns_plot = sns.heatmap(agreement.rename({'true_label_id': 'Truth'}, axis=1).rename({'true_label_id': 'Truth'}, axis=0), annot=True)
            fig = sns_plot.get_figure()
            fig_bytes = BytesIO()
            fig.savefig(fig_bytes, format='png')
            fig_bytes.seek(0)
            base64b = base64.b64encode(fig_bytes.read())
            fig_bytes.close()
            plt.clf()
            return base64b


        annotations_df = get_annotations(cursor, project_id)
        # annotations_df.to_csv(r'C:\Users\omri.allouche\Downloads\labeler_agreement.csv')
        annotations_df = annotations_df.drop_duplicates(['document_id', 'user_id'])
        annotations_df['is_correct'] = [int(x) for x in annotations_df['label_id']==annotations_df['true_label_id']]
        user_truth_agreement = annotations_df[ pd.notnull(annotations_df['true_label_id']) ].groupby('user_id')['is_correct'].agg(['count', 'mean'])

        document_annotations_by_labeler = annotations_df.pivot(index='document_id', columns='user_id', values='label_id')
        document_annotations_by_labeler = pd.merge(left=document_annotations_by_labeler, right=annotations_df.set_index('document_id')[['true_label_id']], left_index=True, right_index=True)
        documents_agreement_df = add_agreement_columns(document_annotations_by_labeler, 'true_label_id')
        users_agreement_kappa = create_kappa_comparison_df(document_annotations_by_labeler)
        average_kappa_agreement_per_labeler = compute_average_agreement_per_labeler(users_agreement_kappa)

        users = get_users_data(cursor, project_id)
        users['average_kappa_agreement'] = average_kappa_agreement_per_labeler
        users['agreement_with_truth'] = user_truth_agreement['mean']
        users['num_documents_with_truth_labels'] = user_truth_agreement['count']
        users = users.reset_index()

        num_truth_annotations = annotations_df['true_label_id'].count()
        response = {
            'num_truth_annotations': num_truth_annotations,
            'users': users.fillna(0).T.to_dict(),
            'document_agreement': documents_agreement_df.fillna(0).T.to_dict(),
            'matrix': plot_agreement_matrix(users_agreement_kappa),
            'users_agreement': users_agreement_kappa.fillna(1).to_dict()
        }
        return Response(response)

class LabelAdminAPI(APIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get(self, request, *args, **kwargs):
        # p = get_object_or_404(Project, pk=self.kwargs['project_id'])
        z = get_labels_admin(project_id=self.kwargs['project_id'])
        response = {'dataframe': z}
        return Response(response)

class UserInfo(APIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get(self, request, *args, **kwargs):
        user_annots_sql = '''
        SELECT server_documentannotation.document_id,
                server_documentannotation.label_id,
                COUNT(DISTINCT user_id) AS num_labelers,
                server_documentannotation.created_date_time AS last_annotation_date,
                substr(server_document.text, 0, 60) AS document_text,
                server_documentgoldannotation.label_id as ground_truth,
                server_documentmlmannotation.prob as model_confidence
            FROM server_documentannotation
            LEFT JOIN server_document ON server_document.id = server_documentannotation.document_id
            LEFT JOIN server_documentgoldannotation ON server_documentgoldannotation.document_id = server_documentannotation.document_id
            LEFT JOIN server_documentmlmannotation ON server_documentmlmannotation.document_id = server_documentannotation.document_id
            LEFT JOIN auth_user ON auth_user.id = server_documentannotation.user_id
            WHERE server_document.project_id = {project_id} AND server_documentannotation.user_id = {user_id}
            GROUP BY server_documentannotation.document_id, 
            server_documentannotation.label_id, 
            server_document.text, 
            server_documentgoldannotation.label_id, 
            server_documentmlmannotation.prob,
            server_documentannotation.created_date_time'''.format(project_id=self.kwargs['project_id'], user_id=self.kwargs['user_id'])
        cursor = connection.cursor()
        cursor.execute(user_annots_sql)
        df = pd.DataFrame(cursor.fetchall(), columns=[
            'document_id', 'label_id', 'num_labelers', 'last_annotation_date', 'snippet', 'ground_truth', 'model_confidence'
        ])
        z = df.sort_values(['document_id', 'num_labelers'], ascending=[True, False]) \
            .groupby(['document_id']) \
            .agg({
            'label_id': [('top_label', lambda x: x.iloc[0])],
            'num_labelers': [
                ('agreement', lambda x: round(x.iloc[0] / sum(x))),
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
        z['ground_truth'] = z['ground_truth'].fillna(-1)

        response = {'dataframe': z}
        return Response(response)

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
            server_documentannotation.user_id,
            server_documentannotation.label_id
            FROM
            server_document
            LEFT JOIN server_documentannotation ON server_documentannotation.document_id = server_document.id 
              -- AND server_documentannotation.user_id = {user_id}
            WHERE server_document.project_id = {project_id}'''.format(user_id=request.user.id, project_id=project_id)

        doc_annotations_gold_query = '''SELECT
            server_document.id,
            server_document.text,
            'gold_label' as user_id,
            server_documentgoldannotation.label_id
            FROM
            server_documentgoldannotation
            LEFT JOIN server_document ON server_documentgoldannotation.document_id = server_document.id
            WHERE server_document.project_id = {project_id}
            '''.format(project_id=project_id)

        if not os.path.isdir(ML_FOLDER):
            os.makedirs(ML_FOLDER)

        cursor.execute(doc_annotations_gold_query)
        gold_annotations = cursor.fetchall()
        cursor.execute(doc_annotations_query)
        user_annotations = cursor.fetchall()

        cols = ['document_id', 'text', 'user_id', 'label_id']
        df_gold_annotations = pd.DataFrame(gold_annotations, columns=cols).set_index('document_id')
        df_user_annotations = pd.DataFrame(user_annotations, columns=cols).set_index('document_id')
        df_user_annotations['gold_label'] = df_gold_annotations['label_id']
        df_user_annotations = df_user_annotations[ pd.isnull(df_user_annotations['gold_label']) ]
        df_user_annotations = df_user_annotations.reset_index()[cols]
        df_gold_annotations = df_gold_annotations.reset_index()
        df = pd.concat([df_user_annotations[cols], df_gold_annotations])

        print( df.groupby('label_id')[['user_id', 'document_id']].count())
        df = df.drop_duplicates(['document_id', 'user_id'], keep='last')
        print( df.groupby('label_id')[['user_id', 'document_id']].count())
        # This step would keep only annotations marked as Gold truth in the set, without using them for training the model
        # df.to_csv(os.path.join(ML_FOLDER, INPUT_FILE.replace('.csv', '_full.csv')), encoding='utf-8')
        df = df.drop_duplicates('document_id', keep='last')
        print( df.groupby('label_id')[['user_id', 'document_id']].count())
        df.to_csv(INPUT_FILE, encoding='utf-8')

        # result = run_model_on_file(INPUT_FILE, OUTPUT_FILE, user_id=request.user.id, project_id=project_id)
        active_learning_function = Project.project_types[ p.project_type ]['active_learning_function']
        result = active_learning_function(
            input_filename = INPUT_FILE,
            output_filename = OUTPUT_FILE,
            user_id = request.user.id,
            project_id = project_id,
            run_on_entire_dataset = (p.use_machine_model_sort or p.show_ml_model_prediction)
        )

        if p.use_machine_model_sort or p.show_ml_model_prediction:
            print('Saving annotations to DB...')
            try:
                reader = csv.DictReader(open(os.path.join(ML_FOLDER, OUTPUT_FILE), 'r', encoding='utf-8'))
                DocumentMLMAnnotation.objects.all().delete()

                batch_size = 1000
                new_annotations = (DocumentMLMAnnotation(
                    document=Document.objects.get(pk=int(float(row['document_id']))),
                    label=Label.objects.get(pk=int(float(row['label_id']))),
                    prob=row['prob']
                ) for row in reader if row['document_id']!='')

                while True:
                    print('processing batch...')
                    batch = list(islice(new_annotations, batch_size))
                    if not batch:
                        break
                    DocumentMLMAnnotation.objects.bulk_create(batch, batch_size)
            except Exception as e:
                print(e)

        # os.remove(INPUT_FILE)
        # os.remove(OUTPUT_FILE)
        print('Done!')
        return Response({'result': '<pre>'+result+'</pre>'})

class ProjectStatsAPI(APIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        project_type = Project.project_types[project.project_type]['type']

        if project_type=='DocumentClassification':
            query = """
    SELECT
        server_documentannotation.user_id,
        auth_user.username AS username,
        server_documentannotation.label_id,
        server_label.text AS label_text,
        COUNT(DISTINCT server_document.id) AS num_documents,
        COUNT(server_documentannotation.id) AS num_annotations
    
    FROM server_documentannotation
        LEFT JOIN server_document ON server_documentannotation.document_id = server_document.id
        LEFT JOIN server_label ON server_documentannotation.label_id = server_label.id
        LEFT JOIN auth_user ON auth_user.id = server_documentannotation.user_id
    WHERE server_document.project_id = {}
    GROUP BY user_id, username, label_id, label_text
            """.format(int(project.id))
            columns = ['user_id', 'username', 'label_id', 'label_text', 'num_documents', 'num_annotations']

        elif project_type=='SequenceLabeling':
            query = """
            SELECT
                server_documentannotation.user_id,
                auth_user.username AS username,
                server_documentannotation.label_id,
                server_label.text AS label_text,
                COUNT(DISTINCT server_document.id) AS num_documents,
                COUNT(server_documentannotation.id) AS num_annotations

            FROM server_sequenceannotation AS server_documentannotation
                LEFT JOIN server_document ON server_documentannotation.document_id = server_document.id
                LEFT JOIN server_label ON server_documentannotation.label_id = server_label.id
                LEFT JOIN auth_user ON auth_user.id = server_documentannotation.user_id
            WHERE server_document.project_id = {}
            GROUP BY user_id, username, label_id, label_text
                    """.format(int(project.id))
            columns = ['user_id', 'username', 'label_id', 'label_text', 'num_documents', 'num_annotations']

        elif project_type=='Seq2seq':
            query = """
            SELECT
                server_documentannotation.user_id,
                auth_user.username AS username,
                COUNT(DISTINCT server_document.id) AS num_documents,
                COUNT(server_documentannotation.id) AS num_annotations

            FROM server_seq2seqannotation AS server_documentannotation
                LEFT JOIN server_document ON server_documentannotation.document_id = server_document.id
                LEFT JOIN auth_user ON auth_user.id = server_documentannotation.user_id
            WHERE server_document.project_id = {}
            GROUP BY user_id, username
                    """.format(int(project.id))
            columns = ['user_id', 'username', 'num_documents', 'num_annotations']

        else:
            raise Exception('Unidentified project type')

        cursor = connection.cursor()
        cursor.execute(query)
        df = pd.DataFrame(cursor.fetchall(), columns=columns)
        labels = df.groupby('label_text')['num_documents'].sum()
        users = df.groupby('username')['num_documents'].sum()
        # user_label_pivot_table = df.pivot(index='user_name', columns='label_text', values='num_documents').fillna(0)
        user_label_pivot_table = []
        response = {
            'label': {
                'labels': labels.index,
                'data': labels.values
            },
            'user': {
                'users': users.index,
                'data': users.values
            },
            'user_label_pivot_table': user_label_pivot_table
        }

        return Response(response)


def get_class_weights(project_id):
    filename = os.path.join(ML_FOLDER, 'ml_logistic_regression_weights_{project_id}.csv').format(project_id=project_id)
    if (os.path.isfile(filename)):
        data = pd.read_csv(os.path.abspath(filename))
        data['importance'] = data['importance'].apply(lambda x: round(x,2))
        data['feature_name'] = data['feature_name'].str.replace('processed_text_w_', '')
        class_weights = data.set_index('feature_name')
        return class_weights
    else:
        print('Missing class weights filename...')
    return pd.DataFrame([], columns=['importance', 'feature_name']).set_index('feature_name')

class ClassWeightsApi(APIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser)

    def get(self, request, *args, **kwargs):
        weights = get_class_weights(self.kwargs['project_id'])
        # resp = None
        # if (weights is not None):
        #     resp = weights.to_dict()
        return Response({'weights': weights.reset_index().values})


class DocumentExplainAPI(generics.RetrieveUpdateDestroyAPIView):
    project_id = 0
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser)

    def get(self, request, *args, **kwargs):
        d = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        self.project_id = self.kwargs['project_id']
        doc_text_splited = d.text.split(' ')
        format_str = '<span style="background-color:{bg_color}; color:{text_color}" title="Weight:{weight} for class {title}">{w}</span>'

        labels = Label.objects.all()
        labels = {row['id']: row for row in (labels.values())}
        text = []
        class_weights = get_class_weights(self.project_id)
        if class_weights is not None:
            for w in doc_text_splited:
                w_clean = w.lower().replace(',','').replace('.','')
                if w_clean in class_weights.index:
                    row = class_weights.loc[w_clean]
                    # weight = row['weight']
                    weight = row['importance']
                    label_id = row['class']
                    label_bg = labels[label_id]['background_color']
                    label_text_color = labels[label_id]['text_color']
                    label_title = labels[label_id]['text']
                    if weight > 0.2:
                        text.append(format_str.format(
                            w=w,
                            bg_color=label_bg,
                            text_color=label_text_color,
                            title=label_title,
                            weight=weight
                        ))
                    else:
                        text.append(w)
                else:
                    text.append(w)

        response = {'document': ' '.join(text)}
        return Response(response)

class DocumentLabelersAPI(generics.RetrieveUpdateDestroyAPIView):
    project_id = 0
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def get(self, request, *args, **kwargs):
        d = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        self.project_id = self.kwargs['project_id']
        annots = d.get_annotations()
        ret = []
        for a in annots:
            ret.append({
                'user_id': a.user.id,
                'user_name': a.user.username,
                'label_id': a.label.id
            })
        response = {'document_annotations': ret}
        return Response(response)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        queryset = self.queryset.filter(project.id)
        return queryset


class ProjectsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        queryset = self.queryset.filter(project.id)
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
            print(int(is_null))
            queryset = project.get_documents(is_null=is_null, user=self.request.user.id).distinct()

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

        if project.shuffle_documents:
            print('order randomly')
            queryset = queryset.order_by('?')

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
