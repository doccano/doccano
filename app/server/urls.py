from django.urls import path
from rest_framework import routers

from .views import IndexView
from .views import ProjectView, DatasetView, DataUpload, LabelView, StatsView, GuidelineView
from .views import ProjectsView, DataDownload
from .views import DemoTextClassification, DemoNamedEntityRecognition, DemoTranslation
from .api import ProjectViewSet, LabelList, ProjectStatsAPI, LabelDetail, \
    AnnotationList, AnnotationDetail, DocumentList, AutoLabeling, AnnotationConfirmation

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/projects/<int:project_id>/stats/', ProjectStatsAPI.as_view(), name='stats-api'),
    path('api/projects/<int:project_id>/labels/', LabelList.as_view(), name='labels'),
    path('api/projects/<int:project_id>/labels/<int:label_id>', LabelDetail.as_view(), name='label'),
    path('api/projects/<int:project_id>/docs/', DocumentList.as_view(), name='docs'),
    path('api/projects/<int:project_id>/docs/<int:doc_id>/annotations/', AnnotationList.as_view(), name='annotations'),
    path('api/projects/<int:project_id>/docs/<int:doc_id>/annotations/<int:annotation_id>', AnnotationDetail.as_view(), name='ann'),
    path('api/projects/<int:project_id>/auto-labeling/<int:doc_id>/', AutoLabeling.as_view(), name='auto-labeling'),
    path('api/projects/<int:project_id>/annotationconfirmation/<int:doc_id>/', AnnotationConfirmation.as_view(), name='annotation-confirmation'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('projects/<int:project_id>/download', DataDownload.as_view(), name='download'),
    path('projects/<int:project_id>/', ProjectView.as_view(), name='annotation'),
    path('projects/<int:project_id>/docs/', DatasetView.as_view(), name='dataset'),
    path('projects/<int:project_id>/docs/create', DataUpload.as_view(), name='upload'),
    path('projects/<int:project_id>/labels/', LabelView.as_view(), name='label-management'),
    path('projects/<int:project_id>/stats/', StatsView.as_view(), name='stats'),
    path('projects/<int:project_id>/guideline/', GuidelineView.as_view(), name='guideline'),
    path('demo/text-classification/', DemoTextClassification.as_view(), name='demo-text-classification'),
    path('demo/named-entity-recognition/', DemoNamedEntityRecognition.as_view(), name='demo-named-entity-recognition'),
    path('demo/translation/', DemoTranslation.as_view(), name='demo-translation'),
]
