from typing import Any, Dict, Iterator, List

import pandas as pd
from django.db.models.query import QuerySet

from .labels import Labels
from examples.models import Example


def filter_examples(examples: QuerySet[Example], is_collaborative=False, confirmed_only=False, user=None):
    if is_collaborative and confirmed_only:
        return examples.exclude(states=None)
    elif not is_collaborative and confirmed_only:
        assert user is not None
        return examples.filter(states__confirmed_by=user)
    else:
        return examples


class Dataset:
    def __init__(self, examples: QuerySet[Example], labels: List[Labels]):
        self.examples = examples
        self.labels = labels

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        for example in self.examples:
            data = {"id": example.id, "data": example.text, **example.meta}
            for labels in self.labels:
                data.update(**labels.find_by(example.id))
            yield data

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self)
