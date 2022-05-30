from typing import Dict, List

from pydantic import UUID4

from examples.models import Example


class Examples:
    def __init__(self, examples: List[Example]):
        self.examples = examples
        self.uuid_to_example: Dict[UUID4, Example] = {}

    def __getitem__(self, uuid: UUID4) -> Example:
        return self.uuid_to_example[uuid]

    def __contains__(self, uuid: UUID4) -> bool:
        return uuid in self.uuid_to_example

    def save(self):
        examples = Example.objects.bulk_create(self.examples)
        self.uuid_to_example = {example.uuid: example for example in examples}
