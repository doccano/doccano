import json
from typing import Any, Dict, List


class Record:

    def __init__(self,
                 id: int,
                 data: str,
                 label: List[Any],
                 user: str,
                 metadata: Dict[Any, Any]):
        self.id = id
        self.data = data
        self.label = label
        self.user = user
        self.metadata = metadata

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'data': self.data,
            'label': self.label,
            'user': self.user,
            'metadata': self.metadata
        })
