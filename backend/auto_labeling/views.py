import json

import botocore.exceptions
import requests
from auto_labeling_pipeline.mappings import MappingTemplate
from auto_labeling_pipeline.menu import Options
from auto_labeling_pipeline.models import RequestModelFactory
from auto_labeling_pipeline.postprocessing import PostProcessor
from django.shortcuts import get_object_or_404
from django_drf_filepond.models import TemporaryUpload
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import (
    AWSTokenError,
    ResponseJSONDecodeError,
    SampleDataException,
    TemplateMappingError,
    URLConnectionError,
)
from .models import AutoLabelingConfig
from .pipeline.execution import execute_pipeline, get_label_collection
from .serializers import AutoLabelingConfigSerializer
from projects.models import Project
from projects.permissions import IsProjectAdmin, IsProjectMember


class TemplateListAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request: Request, *args, **kwargs):
        task_name = request.query_params.get("task_name")
        options = Options.filter_by_task(task_name=task_name)
        option_names = [o.name for o in options]
        return Response(option_names, status=status.HTTP_200_OK)


class TemplateDetailAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        option = Options.find(option_name=self.kwargs["option_name"])
        return Response(option.to_dict(), status=status.HTTP_200_OK)


class ConfigList(generics.ListCreateAPIView):
    serializer_class = AutoLabelingConfigSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get_queryset(self):
        return AutoLabelingConfig.objects.filter(project=self.kwargs["project_id"])

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs["project_id"])


class ConfigDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AutoLabelingConfig.objects.all()
    serializer_class = AutoLabelingConfigSerializer
    lookup_url_kwarg = "config_id"
    permission_classes = [IsAuthenticated & IsProjectAdmin]


class RestAPIRequestTesting(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_id"])

    def create_model(self):
        model_name = self.request.data.get("model_name")
        model_attrs = self.request.data.get("model_attrs")

        # Convert model_attrs from UI format (list of objects) to dict format
        attrs_dict = {}
        if isinstance(model_attrs, list):
            # Frontend sends as [{name: "url", value: "..."}, ...]
            for attr in model_attrs:
                if isinstance(attr, dict) and "name" in attr:
                    value = attr.get("value", "")
                    # Convert empty string to empty dict for object fields
                    if value == "" or value == []:
                        value = {}
                    attrs_dict[attr["name"]] = value
        else:
            # Already in dict format
            attrs_dict = model_attrs

        # For CustomRESTRequestModel, provide defaults for optional fields if not present
        if model_name == "Custom REST Request":
            if "params" not in attrs_dict or not isinstance(attrs_dict.get("params"), dict):
                attrs_dict["params"] = {}
            if "headers" not in attrs_dict or not isinstance(attrs_dict.get("headers"), dict):
                attrs_dict["headers"] = {}
            if "body" not in attrs_dict or not isinstance(attrs_dict.get("body"), dict):
                attrs_dict["body"] = {}

        try:
            model = RequestModelFactory.create(model_name, attrs_dict)
            return model
        except Exception as e:
            model = RequestModelFactory.find(model_name)
            schema = model.schema()
            required_fields = ", ".join(schema["required"]) if "required" in schema else ""
            raise ValidationError(
                "The attributes does not match the model. "
                "You need to correctly specify the required fields: {}".format(required_fields)
            )

    def send_request(self, model, example):
        try:
            # For CustomRESTRequestModel, if body is empty, automatically populate it with text
            if hasattr(model, 'body') and isinstance(model.body, dict) and not model.body:
                # Create a copy to avoid modifying the original model
                import copy
                model = copy.deepcopy(model)
                model.body = {"text": example}

            return model.send(example)
        except requests.exceptions.ConnectionError:
            raise URLConnectionError
        except botocore.exceptions.ClientError:
            raise AWSTokenError()
        except json.decoder.JSONDecodeError:
            raise ResponseJSONDecodeError()
        except Exception as e:
            raise e

    def prepare_example(self):
        text = self.request.data["text"]
        if self.project.is_text_project:
            return text
        else:
            tu = TemporaryUpload.objects.get(upload_id=text)
            return tu.get_file_path()

    def post(self, *args, **kwargs):
        model = self.create_model()
        example = self.prepare_example()
        response = self.send_request(model=model, example=example)
        return Response(response, status=status.HTTP_200_OK)


class LabelExtractorTesting(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, *args, **kwargs):
        response = self.request.data["response"]
        template = self.request.data["template"]
        task_type = self.request.data["task_type"]
        label_collection = get_label_collection(task_type)
        template = MappingTemplate(label_collection=label_collection, template=template)
        try:
            labels = template.render(response)
        except json.decoder.JSONDecodeError:
            raise TemplateMappingError()
        if not labels.dict():
            raise SampleDataException()
        return Response(labels.dict(), status=status.HTTP_200_OK)


class LabelMapperTesting(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, *args, **kwargs):
        response = self.request.data["response"]
        task_type = self.request.data["task_type"]
        label_mapping = self.request.data["label_mapping"]
        label_collection = get_label_collection(task_type)
        labels = label_collection(response)
        post_processor = PostProcessor(label_mapping)
        labels = post_processor.transform(labels)
        return Response(labels.dict(), status=status.HTTP_200_OK)


class AutomatedLabeling(generics.CreateAPIView):
    permission_classes = [IsAuthenticated & IsProjectMember]
    swagger_schema = None

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        example = project.examples.get(pk=self.request.query_params["example"])
        configs = AutoLabelingConfig.objects.filter(project=project)
        # Todo: make async calls or celery tasks to reduce waiting time.
        for config in configs:
            labels = execute_pipeline(example.data, config=config)
            labels.save(project, example, self.request.user)
        return Response({"ok": True}, status=status.HTTP_201_CREATED)
