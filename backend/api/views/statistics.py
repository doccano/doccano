import collections

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Project
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
            progress = self.progress(project=p)
            response.update(progress)

        if include:
            response = {key: value for (key, value) in response.items() if key in include}

        return Response(response)

    @staticmethod
    def _get_user_completion_data(annotation_class, annotation_filter):
        all_annotation_objects = annotation_class.objects.filter(annotation_filter)
        set_user_data = collections.defaultdict(set)
        for ind_obj in all_annotation_objects.values('user__username', 'example__id'):
            set_user_data[ind_obj['user__username']].add(ind_obj['example__id'])
        return {i: len(set_user_data[i]) for i in set_user_data}

    def progress(self, project):
        docs = project.examples
        annotation_class = project.get_annotation_class()
        total = docs.count()
        annotation_filter = Q(example_id__in=docs.all())
        user_data = self._get_user_completion_data(annotation_class, annotation_filter)
        if not project.collaborative_annotation:
            annotation_filter &= Q(user_id=self.request.user)
        done = annotation_class.objects.filter(annotation_filter)\
            .aggregate(Count('example', distinct=True))['example__count']
        remaining = total - done
        return {'total': total, 'remaining': remaining, 'user': user_data}

    def label_per_data(self, project):
        annotation_class = project.get_annotation_class()
        return annotation_class.objects.get_label_per_data(project=project)
