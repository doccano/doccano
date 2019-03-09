import csv
import os
import operator
import nltk
import simplejson
import gensim.downloader as api

from collections import Counter
from itertools import chain
from itertools import islice

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, generics, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project, Label, Document, DocumentAnnotation
from .permissions import IsAdminUserAndWriteOnly, IsProjectUser, IsOwnAnnotation
from .serializers import ProjectSerializer, LabelSerializer, Word2vecSerializer
from .filters import ExcludeSearchFilter

from classifier.text.text_classifier import run_model_on_file

from gensim.models import KeyedVectors


ML_FOLDER = "ml_models"

OUTPUT_FILE = "ml_out.csv"
INPUT_FILE = "ml_input.csv"


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, IsAdminUserAndWriteOnly)

    def get_queryset(self):
        queryset = self.request.user.projects
        return queryset

    @action(methods=["get"], detail=True)
    def progress(self, request, pk=None):
        project = self.get_object()
        return Response(project.get_progress(self.request.user))


class LabelList(generics.ListCreateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get_queryset(self):
        queryset = self.queryset.filter(project=self.kwargs["project_id"])

        return queryset

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        serializer.save(project=project)


class RunModelAPI(APIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get(self, request, *args, **kwargs):
        p = get_object_or_404(Project, pk=self.kwargs["project_id"])
        docs = [doc for doc in p.documents.all()]
        doc_labels = [[a.label.id for a in doc.get_annotations()] for doc in docs]
        doc_ids = [doc.id for doc in docs]
        doc_texts = [doc.text for doc in docs]
        if not os.path.isdir(ML_FOLDER):
            os.makedirs(ML_FOLDER)
        with open(
            os.path.join(ML_FOLDER, INPUT_FILE), "w", encoding="utf-8"
        ) as outfile:
            wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
            wr.writerow(["document_id", "text", "label_id"])
            data = list(zip(doc_ids, doc_texts, doc_labels))
            for row in data:
                label_id = None
                if len(row[2]) > 0:
                    label_id = row[2][0]
                wr.writerow([row[0], row[1], label_id])
        users = User.objects.values()
        mlm_user = None
        mlm_id = None
        try:
            mlm_user = User.objects.get(username="MachineLearningModel")
        except User.DoesNotExist:
            print(
                'User "MachineLearningModel" did not exist. Created it automatically.'
            )
            mlm_user = User.objects.create_user(
                username="MachineLearningModel", password="MachineLearningModel"
            )
            mlm_id = mlm_user.pk
        else:
            mlm_id = mlm_user.pk
        result = run_model_on_file(
            os.path.join(ML_FOLDER, INPUT_FILE),
            os.path.join(ML_FOLDER, OUTPUT_FILE),
            mlm_id,
        )

        reader = csv.DictReader(
            open(os.path.join(ML_FOLDER, OUTPUT_FILE), "r", encoding="utf-8")
        )
        current_anotations = DocumentAnnotation.objects.filter(user=mlm_user)
        if current_anotations.exists():
            current_anotations._raw_delete(current_anotations.db)

        batch_size = 500
        new_annotations = (
            DocumentAnnotation(
                document=Document.objects.get(pk=row["document_id"]),
                label=Label.objects.get(pk=int(float(row["label_id"]))),
                user=mlm_user,
                prob=row["prob"],
            )
            for row in reader
        )
        while True:
            batch = list(islice(new_annotations, batch_size))
            if not batch:
                break
            DocumentAnnotation.objects.bulk_create(batch, batch_size)
        # os.remove(INPUT_FILE)
        # os.remove(OUTPUT_FILE)
        return Response({"result": result})


class ProjectStatsAPI(APIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get(self, request, *args, **kwargs):
        p = get_object_or_404(Project, pk=self.kwargs["project_id"])
        labels = [label.text for label in p.labels.all()]
        users = [user.username for user in p.users.all()]
        docs = [doc for doc in p.documents.all()]
        nested_labels = [[a.label.text for a in doc.get_annotations()] for doc in docs]
        nested_users = [
            [a.user.username for a in doc.get_annotations()] for doc in docs
        ]

        label_count = Counter(chain(*nested_labels))
        label_data = [label_count[name] for name in labels]

        user_count = Counter(chain(*nested_users))
        user_data = [user_count[name] for name in users]

        response = {
            "label": {"labels": labels, "data": label_data},
            "user": {"users": users, "data": user_data},
        }

        return Response(response)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def get_queryset(self):
        queryset = self.queryset.filter(project=self.kwargs["project_id"])
        return queryset


class LabelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def get_queryset(self):
        queryset = self.queryset.filter(project=self.kwargs["project_id"])

        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs["label_id"])
        self.check_object_permissions(self.request, obj)

        return obj


class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    filter_backends = (DjangoFilterBackend, ExcludeSearchFilter, filters.OrderingFilter)
    search_fields = ("text",)
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        self.serializer_class = project.get_document_serializer()

        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        queryset = self.queryset.order_by("doc_annotations__prob").filter(
            project=self.kwargs["project_id"]
        )
        if not self.request.query_params.get("is_checked"):
            if project.use_machine_model_sort:
                try:
                    mlm_user = User.objects.get(username="MachineLearningModel")
                except User.DoesNotExist:
                    mlm_user = None
                if mlm_user:
                    queryset = queryset.filter(doc_annotations__user=mlm_user)
                    queryset = queryset.order_by("doc_annotations__prob")
                    queryset = sorted(
                        queryset, key=lambda x: x.is_labeled_by(self.request.user)
                    )
            return queryset

        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        is_null = self.request.query_params.get("is_checked") == "true"
        queryset = project.get_documents(is_null).distinct()

        return queryset


class AnnotationList(generics.ListCreateAPIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser)

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        self.serializer_class = project.get_annotation_serializer()

        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        document = project.documents.get(id=self.kwargs["doc_id"])
        self.queryset = document.get_annotations()
        self.queryset = self.queryset.filter(user=self.request.user)

        return self.queryset

    def perform_create(self, serializer):
        doc = get_object_or_404(Document, pk=self.kwargs["doc_id"])
        serializer.save(document=doc, user=self.request.user)


class AnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsProjectUser, IsOwnAnnotation)

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        self.serializer_class = project.get_annotation_serializer()

        return self.serializer_class

    def get_queryset(self):
        document = get_object_or_404(Document, pk=self.kwargs["doc_id"])
        self.queryset = document.get_annotations()

        return self.queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs["annotation_id"])
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
    model = api.load("glove-wiki-gigaword-100")
    serializer_class = Word2vecSerializer


    def get_queryset(self):
        w = self.request.GET.get("word", "")
        queryset = self.model.most_similar(positive=[w])
        print(queryset)

        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        response = self.get_object()

        return Response(response)
