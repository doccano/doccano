from django.urls import path
from rest_framework import routers

from .views import IndexView
from .views import ProjectView, DatasetView, DataUpload, LabelView, StatsView, GuidelineView
from .views import ProjectsView, DataDownload, DataDownloadFile
from .views import DemoTextClassification, DemoNamedEntityRecognition, DemoTranslation
from .api import ProjectViewSet, LabelList, StatisticsAPI, LabelDetail, \
    AnnotationList, AnnotationDetail, DocumentList, DocumentDetail, EntityList, EntityDetail, ProjectList, ProjectDetail

router = routers.DefaultRouter()
#router.register(r'projects', ProjectViewSet)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/projects/', ProjectList.as_view(), name='project_list'),
    path('api/projects/<int:project_id>', ProjectDetail.as_view(), name='project_detail'),
    path('api/projects/<int:project_id>/statistics/',
         StatisticsAPI.as_view(), name='statistics'),
    path('api/projects/<int:project_id>/labels/',
         LabelList.as_view(), name='label_list'),
    path('api/projects/<int:project_id>/labels/<int:label_id>/',
         LabelDetail.as_view(), name='label_detail'),
    path('api/projects/<int:project_id>/docs/',
         DocumentList.as_view(), name='doc_list'),
    path('api/projects/<int:project_id>/docs/<int:doc_id>/',
         DocumentDetail.as_view(), name='doc_detail'),
    path('api/projects/<int:project_id>/docs/<int:doc_id>/entities',
         EntityList.as_view(), name='entity_list'),
    path('api/projects/<int:project_id>/docs/<int:doc_id>/entities/<int:entity_id>/',
         EntityDetail.as_view(), name='entity_detail'),
    path('api/projects/<int:project_id>/docs/<int:doc_id>/annotations/',
         AnnotationList.as_view(), name='annotations'),
    path('api/projects/<int:project_id>/docs/<int:doc_id>/annotations/<int:annotation_id>',
         AnnotationDetail.as_view(), name='ann'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('projects/<int:project_id>/download',
         DataDownload.as_view(), name='download'),
    path('projects/<int:project_id>/download_file',
         DataDownloadFile.as_view(), name='download_file'),
    path('projects/<int:project_id>/',
         ProjectView.as_view(), name='annotation'),
    path('projects/<int:project_id>/docs/',
         DatasetView.as_view(), name='dataset'),
    path('projects/<int:project_id>/docs/create',
         DataUpload.as_view(), name='upload'),
    path('projects/<int:project_id>/labels/',
         LabelView.as_view(), name='label-management'),
    path('projects/<int:project_id>/stats/',
         StatsView.as_view(), name='stats'),
    path('projects/<int:project_id>/guideline/',
         GuidelineView.as_view(), name='guideline'),
    path('demo/text-classification/',
         DemoTextClassification.as_view(), name='demo-text-classification'),
    path('demo/named-entity-recognition/',
         DemoNamedEntityRecognition.as_view(), name='demo-named-entity-recognition'),
    path('demo/translation/', DemoTranslation.as_view(), name='demo-translation'),
]
