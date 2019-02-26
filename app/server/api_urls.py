from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .api import ProjectList, ProjectDetail
from .api import LabelList, LabelDetail
from .api import DocumentList, DocumentDetail
from .api import EntityList, EntityDetail
from .api import CoNLLFileUploadAPI
from .api import StatisticsAPI


urlpatterns = [
    path('projects', ProjectList.as_view(), name='project_list'),
    path('projects/<int:project_id>', ProjectDetail.as_view(), name='project_detail'),
    path('projects/<int:project_id>/statistics',
         StatisticsAPI.as_view(), name='statistics'),
    path('projects/<int:project_id>/labels',
         LabelList.as_view(), name='label_list'),
    path('projects/<int:project_id>/labels/<int:label_id>',
         LabelDetail.as_view(), name='label_detail'),
    path('projects/<int:project_id>/docs',
         DocumentList.as_view(), name='doc_list'),
    path('projects/<int:project_id>/docs/<int:doc_id>',
         DocumentDetail.as_view(), name='doc_detail'),
    path('projects/<int:project_id>/docs/<int:doc_id>/entities',
         EntityList.as_view(), name='entity_list'),
    path('projects/<int:project_id>/docs/<int:doc_id>/entities/<int:entity_id>',
         EntityDetail.as_view(), name='entity_detail'),
    path('projects/<int:project_id>/conll_uploader',
         CoNLLFileUploadAPI.as_view(), name='conll_uploader'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'xml'])
