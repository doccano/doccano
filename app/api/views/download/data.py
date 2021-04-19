from typing import Any, Dict, List


class Record:

    def __init__(self,
                 id: int,
                 data: str,
                 label: List[Any],
                 user: str,
                 metadata: Dict[Any, Any]):
        self._id = id
        self._data = data
        self._label = label
        self._user = user
        self._metadata = metadata

    def __str__(self):
        return f'{self._data}\t{self._label}'
