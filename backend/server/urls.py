from django.urls import path

from .views import IndexView
from .views import ProjectView, DatasetView, DataUpload, LabelView, StatsView, GuidelineView, UsersView
from .views import ProjectsView, DataDownload
from .views import DemoTextClassification, DemoNamedEntityRecognition, DemoTranslation


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('projects/<int:project_id>/docs/download',
         DataDownload.as_view(), name='download'),
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
    path('projects/<int:project_id>/users/',
         UsersView.as_view(), name='users'),
    path('demo/text-classification/',
         DemoTextClassification.as_view(), name='demo-text-classification'),
    path('demo/named-entity-recognition/',
         DemoNamedEntityRecognition.as_view(), name='demo-named-entity-recognition'),
    path('demo/translation/', DemoTranslation.as_view(), name='demo-translation'),
]
