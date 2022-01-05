import abc

from django.conf import settings
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import (Annotation, Category, Example, ExampleState, Project,
                      RoleMapping, Span)
from ..permissions import IsInProjectReadOnlyOrAdmin


class StatisticsAPI(APIView):
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get(self, request, *args, **kwargs):
        p = get_object_or_404(Project, pk=self.kwargs['project_id'])

        include = set(request.GET.getlist('include'))
        response = {}

        if not include or 'label' in include:
            label_count, user_count = self.label_per_data(p)
            response['label'] = label_count
            # TODO: Make user_label count chart
            response['user_label'] = user_count

        if not include or 'total' in include or 'remaining' in include or 'user' in include:
            progress = self.progress()
            response.update(progress)

        if not include or 'confirmed_count' in include:
            confirmed_count = self.confirmed_count(p)
            response['confirmed_count'] = confirmed_count

        if include:
            response = {key: value for (key, value) in response.items() if key in include}

        return Response(response)

    def progress(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        examples = Example.objects.filter(project=self.kwargs['project_id']).values('id')
        total = examples.count()
        done = ExampleState.objects.count_done(examples)
        done_by_user = ExampleState.objects.measure_member_progress(examples, project.users.all())
        remaining = total - done
        return {'total': total, 'remaining': remaining, 'user': done_by_user}

    def label_per_data(self, project):
        return {}, {}

    def confirmed_count(self, project):
        confirmed_count = {
            settings.ROLE_ANNOTATOR: 0,
            settings.ROLE_ANNOTATION_APPROVER: 0,
            settings.ROLE_PROJECT_ADMIN: 0,
        }
        # Todo: convert to one query
        count_by_user = ExampleState.objects.filter(example__project=project)\
            .values('confirmed_by')\
            .annotate(total=Count('confirmed_by'))
        for record in count_by_user:
            mapping = RoleMapping.objects.get(project=project, user=record['confirmed_by'])
            confirmed_count[mapping.role.name] += record['total']
        return confirmed_count


class ProgressAPI(APIView):
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get(self, request, *args, **kwargs):
        examples = Example.objects.filter(project=self.kwargs['project_id']).values('id')
        total = examples.count()
        done = ExampleState.objects.count_done(examples, user=self.request.user)
        return {'total': total, 'remaining': total - done}


class MemberProgressAPI(APIView):
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        examples = Example.objects.filter(project=self.kwargs['project_id']).values('id')
        data = ExampleState.objects.measure_member_progress(examples, project.users.all())
        return Response(data=data, status=status.HTTP_200_OK)


class LabelFrequency(abc.ABC, APIView):
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]
    model = Annotation

    def get(self, request, *args, **kwargs):
        examples = Example.objects.filter(project=self.kwargs['project_id']).values('id')
        return self.model.objects.calc_label_frequency(examples)


class DocTypeFrequency(LabelFrequency):
    model = Category


class SpanTypeFrequency(LabelFrequency):
    model = Span
