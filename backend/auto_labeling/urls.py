from django.urls import path

from .views import (AutoLabelingConfigDetail, AutoLabelingConfigTest, AutoLabelingAnnotation, AutoLabelingMappingTest,
                    AutoLabelingTemplateListAPI, AutoLabelingTemplateDetailAPI, AutoLabelingConfigList,
                    AutoLabelingConfigParameterTest, AutoLabelingTemplateTest)

urlpatterns = [
    path(
        route='auto-labeling-templates',
        view=AutoLabelingTemplateListAPI.as_view(),
        name='auto_labeling_templates'
    ),
    path(
        route='auto-labeling-templates/<str:option_name>',
        view=AutoLabelingTemplateDetailAPI.as_view(),
        name='auto_labeling_template'
    ),
    path(
        route='auto-labeling-configs',
        view=AutoLabelingConfigList.as_view(),
        name='auto_labeling_configs'
    ),
    path(
        route='auto-labeling-configs/<int:config_id>',
        view=AutoLabelingConfigDetail.as_view(),
        name='auto_labeling_config'
    ),
    path(
        route='auto-labeling-config-testing',
        view=AutoLabelingConfigTest.as_view(),
        name='auto_labeling_config_test'
    ),
    path(
        route='examples/<int:example_id>/auto-labeling',
        view=AutoLabelingAnnotation.as_view(),
        name='auto_labeling_annotation'
    ),
    path(
        route='auto-labeling-parameter-testing',
        view=AutoLabelingConfigParameterTest.as_view(),
        name='auto_labeling_parameter_testing'
    ),
    path(
        route='auto-labeling-template-testing',
        view=AutoLabelingTemplateTest.as_view(),
        name='auto_labeling_template_test'
    ),
    path(
        route='auto-labeling-mapping-testing',
        view=AutoLabelingMappingTest.as_view(),
        name='auto_labeling_mapping_test'
    )
]
