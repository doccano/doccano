from collections import Counter

from django.conf import settings
from django.db.models import Count, Manager


class AnnotationManager(Manager):

    def calc_label_frequency(self, examples):
        """Calculate label frequencies.

        Args:
            examples: example queryset.

        Returns:
            label frequency.

        Examples:
            >>> {'positive': 3, 'negative': 4}
        """
        freq = Counter()
        annotations = self.filter(example_id__in=examples)
        for d in annotations.values('label__text').annotate(Count('label')):
            freq[d['label__text']] += d['label__count']
        return freq

    def calc_user_frequency(self, examples):
        """Calculate user frequencies.

        Args:
            examples: example queryset.

        Returns:
            user frequency.

        Examples:
            >>> {'mary': 3, 'john': 4}
        """
        freq = Counter()
        annotations = self.filter(example_id__in=examples)
        for d in annotations.values('user__username').annotate(Count('user')):
            freq[d['user__username']] += d['user__count']
        return freq

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


class ExampleManager(Manager):

    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        super().bulk_create(objs, batch_size=batch_size, ignore_conflicts=ignore_conflicts)
        uuids = [data.uuid for data in objs]
        examples = self.in_bulk(uuids, field_name='uuid')
        return [examples[uid] for uid in uuids]


class ExampleStateManager(Manager):

    def count_done(self, examples, user=None):
        if user:
            queryset = self.filter(example_id__in=examples, confirmed_by=user)
        else:
            queryset = self.filter(example_id__in=examples)
        return queryset.distinct().values('example').count()

    def measure_member_progress(self, examples, members):
        done_count = self.filter(example_id__in=examples)\
            .values('confirmed_by__username')\
            .annotate(total=Count('confirmed_by'))
        response = {
            'total': examples.count(),
            'progress': {
                obj['confirmed_by__username']: obj['total'] for obj in done_count
            }
        }
        for member in members:
            if member.username not in response['progress']:
                response['progress'][member.username] = 0
        return response
