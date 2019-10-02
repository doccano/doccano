from collections import Counter

from django.db.models import Manager, Count


class AnnotationManager(Manager):

    def get_label_per_data(self, project):
        label_count = Counter()
        user_count = Counter()
        docs = project.documents.all()
        annotations = self.filter(document_id__in=docs.all())

        for d in annotations.values('label__text', 'user__username').annotate(Count('label'), Count('user')):
            label_count[d['label__text']] += d['label__count']
            user_count[d['user__username']] += d['user__count']

        return label_count, user_count


class Seq2seqAnnotationManager(Manager):

    def get_label_per_data(self, project):
        label_count = Counter()
        user_count = Counter()
        docs = project.documents.all()
        annotations = self.filter(document_id__in=docs.all())

        for d in annotations.values('text', 'user__username').annotate(Count('text'), Count('user')):
            label_count[d['text']] += d['text__count']
            user_count[d['user__username']] += d['user__count']

        return label_count, user_count
