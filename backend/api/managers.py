from collections import Counter

from django.conf import settings
from django.db.models import Count, Manager


class AnnotationManager(Manager):

    def get_label_per_data(self, project):
        label_count = Counter()
        user_count = Counter()
        docs = project.examples.all()
        annotations = self.filter(example_id__in=docs.all())

        for d in annotations.values('label__text', 'user__username').annotate(Count('label'), Count('user')):
            label_count[d['label__text']] += d['label__count']
            user_count[d['user__username']] += d['user__count']

        return label_count, user_count


class Seq2seqAnnotationManager(Manager):

    def get_label_per_data(self, project):
        label_count = Counter()
        user_count = Counter()
        docs = project.examples.all()
        annotations = self.filter(example_id__in=docs.all())

        for d in annotations.values('text', 'user__username').annotate(Count('text'), Count('user')):
            label_count[d['text']] += d['text__count']
            user_count[d['user__username']] += d['user__count']

        return label_count, user_count


class RoleMappingManager(Manager):

    def can_update(self, project: int, mapping_id: int, rolename: str):
        queryset = self.filter(
            project=project, role__name=settings.ROLE_PROJECT_ADMIN
        )
        if queryset.count() > 1:
            return True
        else:
            mapping = queryset.first()
            if mapping.id == mapping_id and rolename != settings.ROLE_PROJECT_ADMIN:
                return False
            return True
