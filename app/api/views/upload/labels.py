from typing import Dict, List, Optional

from .label import Label


class Labels:

    def __init__(self, labels: List[Label]):
        self.labels = labels

    def replace_label(self, mapping: Optional[Dict[str, int]] = None):
        if not mapping:
            return self
        labels = [label.replace(mapping) for label in self.labels]
        return Labels(labels)

    def dict(self) -> List[dict]:
        return [label.dict() for label in self.labels]
