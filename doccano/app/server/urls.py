from django.urls import path

from .views import IndexView
from .views import AnnotationAPIView, ProgressAPI, SearchAPI, InboxView
from .views import ProjectListView, ProjectAdminView, RawDataAPI, LabelAPI, DataDownloadAPI

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/admin', ProjectAdminView.as_view(), name='project-admin'),
    path('projects/<int:project_id>/download', DataDownloadAPI.as_view(), name='download'),
    path('projects/<int:project_id>/', InboxView.as_view(), name='annotation'),
    path('projects/<int:project_id>/apis/data', AnnotationAPIView.as_view()),
    path('projects/<int:pk>/apis/raw_data', RawDataAPI.as_view(), name='data_api'),
    path('projects/<int:pk>/apis/labels', LabelAPI.as_view(), name='label_api'),
    path('projects/<int:project_id>/apis/progress', ProgressAPI.as_view()),
    path('projects/<int:project_id>/apis/search', SearchAPI.as_view()),
]
