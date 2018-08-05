from django.urls import path

from .views import IndexView
from .views import ProjectView, DatasetView, DatasetUpload, LabelView
from .views import ProjectsView, ProjectAdminView, DataDownload
from rest_framework import routers
from .views import ProjectViewSet
from .views import ProjectLabelsAPI, ProjectLabelAPI, ProjectDocsAPI, AnnotationsAPI, AnnotationAPI


router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/projects/<int:project_id>/labels/', ProjectLabelsAPI.as_view(), name='labels'),
    path('api/projects/<int:project_id>/labels/<int:label_id>', ProjectLabelAPI.as_view(), name='label'),
    path('api/projects/<int:project_id>/docs/', ProjectDocsAPI.as_view(), name='docs'),
    path('api/projects/<int:project_id>/docs/<int:doc_id>/annotations/', AnnotationsAPI.as_view(), name='annotations'),
    path('api/projects/<int:project_id>/docs/<int:doc_id>/annotations/<int:annotation_id>', AnnotationAPI.as_view(), name='ann'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('projects/<int:project_id>/admin', ProjectAdminView.as_view(), name='project-admin'),
    path('projects/<int:project_id>/download', DataDownload.as_view(), name='download'),
    path('projects/<int:project_id>/', ProjectView.as_view(), name='annotation'),
    path('projects/<int:project_id>/docs/', DatasetView.as_view(), name='dataset'),
    path('projects/<int:project_id>/docs/create', DatasetUpload.as_view(), name='upload'),
    path('projects/<int:project_id>/labels/', LabelView.as_view(), name='label-management'),
]
