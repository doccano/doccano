from typing import Dict, List


def append_field(data: List[Dict], **kwargs):
    [d.update(kwargs) for d in data]
    return data
