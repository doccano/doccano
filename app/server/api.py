from collections import Counter
from itertools import chain

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project, Label, Document
from .permissions import IsAdminUserAndWriteOnly, IsProjectUser, IsOwnAnnotation
from .serializers import ProjectSerializer, LabelSerializer
from .classifiers import NERModel


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, IsAdminUserAndWriteOnly)

    def get_queryset(self):
        return self.request.user.projects

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


class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('text', )
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = project.get_document_serializer()

        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset.filter(project=self.kwargs['project_id'])
        if not self.request.query_params.get('is_checked'):
            return queryset

        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        is_null = self.request.query_params.get('is_checked') == 'true'
        queryset = project.get_documents(is_null).distinct()

        return queryset


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


class AutoLabeling(APIView):
    permission_classes = (IsAuthenticated, IsProjectUser)

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        document = project.documents.get(id=self.kwargs['doc_id'])
        queryset = document.get_annotations()
        queryset = queryset.filter(user=self.request.user)

        return queryset

    def get(self, request, *args, **kwargs):
        """
        Return a list of predicted entities.
        """
        # doc = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        # annotations = doc.get_annotations().filter(user=self.request.user)
        # model = NERModel(model='')
        # res = model.predict(doc.text)
        # delete annotations
        # store predicted result to SeqAnnotation
        # return res

        # resに期待する出力
        # [{
        #    'label': int,
        #    'start_offset': int,
        #    'end_offset': int,
        # }]
        # 文書d内のアノテーションをすべて削除
        # serializerを使ってSequenceAnnotationにresの結果を登録
        # serializer.dataを返却
        res = [
            {
                "id": 116,
                "prob": 0.0,
                "label": 7,
                "start_offset": 0,
                "end_offset": 23
            },
            {
                "id": 119,
                "prob": 0.0,
                "label": 8,
                "start_offset": 121,
                "end_offset": 138
            },
            {
                "id": 127,
                "prob": 0.0,
                "label": 8,
                "start_offset": 321,
                "end_offset": 329
            },
            {
                "id": 122,
                "prob": 0.0,
                "label": 9,
                "start_offset": 199,
                "end_offset": 215
            },
            {
                "id": 128,
                "prob": 0.0,
                "label": 9,
                "start_offset": 350,
                "end_offset": 371
            },
            {
                "id": 117,
                "prob": 0.0,
                "label": 10,
                "start_offset": 30,
                "end_offset": 44
            },
            {
                "id": 120,
                "prob": 0.0,
                "label": 10,
                "start_offset": 144,
                "end_offset": 160
            },
            {
                "id": 121,
                "prob": 0.0,
                "label": 10,
                "start_offset": 165,
                "end_offset": 181
            },
            {
                "id": 118,
                "prob": 0.0,
                "label": 12,
                "start_offset": 52,
                "end_offset": 60
            },
            {
                "id": 124,
                "prob": 0.0,
                "label": 12,
                "start_offset": 234,
                "end_offset": 250
            },
            {
                "id": 126,
                "prob": 0.0,
                "label": 12,
                "start_offset": 294,
                "end_offset": 315
            }
        ]
        return Response(res)

    def put(self, request, *args, **kwargs):
        """
        Train a model.
        """
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        doc = project.documents.get(id=self.kwargs['doc_id'])
        annotations = doc.get_annotations().filter(user=self.request.user)
        entities = [(a.start_offset, a.end_offset, a.label.text) for a in annotations]
        labels = project.labels.all()
        train_data = [
            (
                doc.text,
                {
                    'entities': entities
                }
            )
        ]
        model = NERModel()
        for label in labels:
            model.add_label(label.text)
        model.train(train_data)
        print('Trained!')
        return Response([])


class AnnotationConfirmation(APIView):
    """
    This view is used to turn manual annotations (from autolabel functionality)
    into reviewed (manual=False) annotations. Currently gets called when
    the user calls nextPage()
    """
    permission_classes = (IsAuthenticated, IsProjectUser)

    def post(self, request, project_id, doc_id):
        project = get_object_or_404(Project, pk=project_id)
        doc = project.documents.get(id=doc_id)
        annotations = doc.get_annotations().filter(user=self.request.user)
        annotations.update(manual=True)
        return Response([])