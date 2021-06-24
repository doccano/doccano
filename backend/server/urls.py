from django.urls import path

from .views import (DataDownload, DatasetView, DataUpload,
                    DemoNamedEntityRecognition, DemoTextClassification, DemoTextSimilarity,
                    DemoTranslation, GuidelineView, IndexView, LabelView,
                    ProjectsView, ProjectView, StatsView, UsersView)

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
    path('demo/text-similarity/',
         DemoTextSimilarity.as_view(), name='demo-text-similarity'),
    path('demo/named-entity-recognition/',
         DemoNamedEntityRecognition.as_view(), name='demo-named-entity-recognition'),
    path('demo/translation/', DemoTranslation.as_view(), name='demo-translation'),
]
