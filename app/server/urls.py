from django.urls import path

from .views import IndexView
from .views import ProjectView
from .views import ProjectsView, ProjectAdminView, RawDataAPI, DataDownloadAPI
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
    path('projects/<int:pk>/admin', ProjectAdminView.as_view(), name='project-admin'),
    path('projects/<int:project_id>/download', DataDownloadAPI.as_view(), name='download'),
    path('projects/<int:project_id>/', ProjectView.as_view(), name='annotation'),
    path('projects/<int:pk>/apis/raw_data', RawDataAPI.as_view(), name='data_api'),
]
