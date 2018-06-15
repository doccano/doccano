from django.urls import path

from .views import AnnotationView, AnnotationAPIView, ProgressAPI, SearchAPI, InboxView
from .views import ProjectListView, ProjectAdminView, RawDataAPI, LabelAPI, DataDownloadAPI

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('<int:pk>/admin', ProjectAdminView.as_view(), name='project-admin'),
    path('<int:project_id>/', AnnotationView.as_view(), name='annotation'),
    path('<int:project_id>/download', DataDownloadAPI.as_view(), name='download'),
    path('<int:project_id>/inbox', InboxView.as_view(), name='inbox'),
    path('<int:project_id>/apis/data', AnnotationAPIView.as_view()),
    path('<int:pk>/apis/raw_data', RawDataAPI.as_view(), name='data_api'),
    path('<int:pk>/apis/labels', LabelAPI.as_view(), name='label_api'),
    path('<int:project_id>/apis/progress', ProgressAPI.as_view()),
    path('<int:project_id>/apis/search', SearchAPI.as_view()),
]
