from django.urls import path

from .views import (ConfigDetail, FullPipelineTesting, AutomatedDataLabeling, AutomatedCategoryLabeling,
                    AutomatedSpanLabeling, LabelMapperTesting, TemplateListAPI, TemplateDetailAPI, ConfigList,
                    RestAPIRequestTesting, LabelExtractorTesting)

urlpatterns = [
    path(
        route='auto-labeling-templates',
        view=TemplateListAPI.as_view(),
        name='auto_labeling_templates'
    ),
    path(
        route='auto-labeling-templates/<str:option_name>',
        view=TemplateDetailAPI.as_view(),
        name='auto_labeling_template'
    ),
    path(
        route='auto-labeling-configs',
        view=ConfigList.as_view(),
        name='auto_labeling_configs'
    ),
    path(
        route='auto-labeling-configs/<int:config_id>',
        view=ConfigDetail.as_view(),
        name='auto_labeling_config'
    ),
    path(
        route='auto-labeling-config-testing',
        view=FullPipelineTesting.as_view(),
        name='auto_labeling_config_test'
    ),
    path(
        route='examples/<int:example_id>/auto-labeling',
        view=AutomatedDataLabeling.as_view(),
        name='auto_labeling_annotation'
    ),
    path(
        route='auto-labeling-parameter-testing',
        view=RestAPIRequestTesting.as_view(),
        name='auto_labeling_parameter_testing'
    ),
    path(
        route='auto-labeling-template-testing',
        view=LabelExtractorTesting.as_view(),
        name='auto_labeling_template_test'
    ),
    path(
        route='auto-labeling-mapping-testing',
        view=LabelMapperTesting.as_view(),
        name='auto_labeling_mapping_test'
    ),
    path(
        route='examples/<int:example_id>/auto-labeling/categories',
        view=AutomatedCategoryLabeling.as_view(),
        name='automated_category_labeling'
    ),
    path(
        route='examples/<int:example_id>/auto-labeling/spans',
        view=AutomatedSpanLabeling.as_view(),
        name='automated_span_labeling'
    )
]
