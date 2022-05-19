from unittest.mock import MagicMock

from label_types.models import CategoryType


class DummyLabelType(CategoryType):
    objects = MagicMock()

    class Meta:
        proxy = True
