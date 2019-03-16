from django.urls import path
from rest_framework import routers

from .views import IndexView
from .views import ProjectView, DatasetView, DataUpload, LabelView, StatsView, GuidelineView, SettingsView, LabelersView, LabelAdminView
from .views import ProjectsView, DataDownload, DataDownloadFile, DocumentExport, DocumentAnnotationExport, LabelExport
from .views import DemoTextClassification, DemoNamedEntityRecognition, DemoTranslation
from .api import ProjectViewSet, LabelList, ProjectStatsAPI, LabelDetail, ProjectDetail, \
    AnnotationList, AnnotationDetail, DocumentList, RunModelAPI, LabelersListAPI, LabelAdminAPI, DocumentExplainAPI, SuggestedTerms

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/projects/<int:project_id>', ProjectDetail.as_view(), name='project-api'),
    path('api/projects/<int:project_id>/stats/', ProjectStatsAPI.as_view(), name='stats-api'),
    path('api/projects/<int:project_id>/runmodel/', RunModelAPI.as_view(), name='runmodel-api'),
    path('api/projects/<int:project_id>/labels/', LabelList.as_view(), name='labels'),
    path('api/projects/<int:project_id>/labels_admin/', LabelAdminAPI.as_view(), name='labels-api'),
    path('api/projects/<int:project_id>/labelers/', LabelersListAPI.as_view(), name='labelers-api'),
    path('api/projects/<int:project_id>/labels/<int:label_id>', LabelDetail.as_view(), name='label'),
    path('api/projects/<int:project_id>/docs/', DocumentList.as_view(), name='docs'),
    path('api/projects/<int:project_id>/docs/<int:doc_id>/annotations/', AnnotationList.as_view(), name='annotations'),
    path('api/projects/<int:project_id>/suggested/', SuggestedTerms.as_view(), name='suggested'),
    path('api/projects/<int:project_id>/docs/<int:doc_id>/explanation/', DocumentExplainAPI.as_view(), name='document_explain'),
    path('api/projects/<int:project_id>/docs/<int:doc_id>/annotations/<int:annotation_id>', AnnotationDetail.as_view(), name='ann'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('projects/<int:project_id>/download', DataDownload.as_view(), name='download'),
    path('projects/<int:project_id>/download_file', DataDownloadFile.as_view(), name='download_file'),
    path('projects/<int:project_id>/export_docs', DocumentExport.as_view(), name='export_docs'),
    path('projects/<int:project_id>/export_annotations', DocumentAnnotationExport.as_view(), name='export_annotations'),
    path('projects/<int:project_id>/export_labels', LabelExport.as_view(), name='export_labels'),
    path('projects/<int:project_id>/', ProjectView.as_view(), name='annotation'),
    path('projects/<int:project_id>/docs/', DatasetView.as_view(), name='dataset'),
    path('projects/<int:project_id>/docs/create', DataUpload.as_view(), name='upload'),
    path('projects/<int:project_id>/labels/', LabelView.as_view(), name='label-management'),
    path('projects/<int:project_id>/labels_admin/', LabelAdminView.as_view(), name='labels-admin'),
    path('projects/<int:project_id>/labelers/', LabelersView.as_view(), name='labelers'),
    path('projects/<int:project_id>/stats/', StatsView.as_view(), name='stats'),
    path('projects/<int:project_id>/guideline/', GuidelineView.as_view(), name='guideline'),
    path('projects/<int:project_id>/settings/', SettingsView.as_view(), name='settings'),
    path('demo/text-classification/', DemoTextClassification.as_view(), name='demo-text-classification'),
    path('demo/named-entity-recognition/', DemoNamedEntityRecognition.as_view(), name='demo-named-entity-recognition'),
    path('demo/translation/', DemoTranslation.as_view(), name='demo-translation'),
]
