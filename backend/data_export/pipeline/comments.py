import abc
from collections import defaultdict
from typing import Dict, List, Tuple

from django.db.models import QuerySet

from data_export.models import ExportedComment, ExportedExample


class Comments(abc.ABC):
    comment_class = ExportedComment
    column = "Comments"
    fields: Tuple[str, ...] = ("example", "user")  # To boost performance

    def __init__(self, examples: QuerySet[ExportedExample], user=None):
        self.comment_groups = defaultdict(list)
        comments = self.comment_class.objects.filter(example__in=examples)
        if user:
            comments = comments.filter(user=user)
        for comment in comments.select_related(*self.fields):
            self.comment_groups[comment.example.id].append(comment)

    def find_by(self, example_id: int) -> Dict[str, List[ExportedComment]]:
        return {self.column: self.comment_groups[example_id]}
