from django.urls import path

from .views import (
    AutomatedLabeling,
    ConfigDetail,
    ConfigList,
    LabelExtractorTesting,
    LabelMapperTesting,
    RestAPIRequestTesting,
    TemplateDetailAPI,
    TemplateListAPI,
)

urlpatterns = [
    path(route="auto-labeling/templates", view=TemplateListAPI.as_view(), name="auto_labeling_templates"),
    path(
        route="auto-labeling/templates/<str:option_name>",
        view=TemplateDetailAPI.as_view(),
        name="auto_labeling_template",
    ),
    path(route="auto-labeling/configs", view=ConfigList.as_view(), name="auto_labeling_configs"),
    path(route="auto-labeling/configs/<int:config_id>", view=ConfigDetail.as_view(), name="auto_labeling_config"),
    path(
        route="auto-labeling/request-testing",
        view=RestAPIRequestTesting.as_view(),
        name="auto_labeling_parameter_testing",
    ),
    path(
        route="auto-labeling/label-extractor-testing",
        view=LabelExtractorTesting.as_view(),
        name="auto_labeling_template_test",
    ),
    path(
        route="auto-labeling/label-mapper-testing", view=LabelMapperTesting.as_view(), name="auto_labeling_mapping_test"
    ),
    path(route="auto-labeling", view=AutomatedLabeling.as_view(), name="auto_labeling"),
]
