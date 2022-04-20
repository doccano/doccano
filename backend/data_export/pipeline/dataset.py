from typing import Any, Dict, Iterator, Type

import pandas as pd
from django.db.models.query import QuerySet

from .labels import Labels
from examples.models import Example


class Dataset:
    def __init__(self, examples: QuerySet[Example], user, label_collection_class: Type[Labels], confirmed_only=False):
        if confirmed_only:
            examples = examples.filter(states__confirmed_by=user)
        self.examples = examples
        self.labels = label_collection_class(examples, user)

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        for example in self.examples:
            yield {"id": example.id, "data": example.text, **example.meta, **self.labels.find_by(example.id)}

    def to_pandas(self) -> pd.DataFrame:
        return pd.DataFrame(self)
