from typing import Dict, List, Optional

from .label import Label


class Labels:

    def __init__(self, labels: List[Label]):
        self.labels = labels

    def replace_label(self, mapping: Optional[Dict[str, int]] = None):
        if not mapping:
            return self
        labels = []
        for label in self.labels:
            try:
                label = label.replace(mapping)
                labels.append(label)
            except KeyError:
                pass
        return Labels(labels)

    def dict(self) -> List[dict]:
        return [label.dict() for label in self.labels]
