import abc
import dataclasses
from typing import List

import numpy as np


@dataclasses.dataclass
class Assignment:
    user: int
    example: int


class BaseStrategy(abc.ABC):
    @abc.abstractmethod
    def assign(self) -> List[Assignment]:
        ...


class WeightedRandomStrategy:
    def __init__(self, dataset_size: int, weights: List[int]):
        assert sum(weights) == 100
        self.dataset_size = dataset_size
        self.weights = weights

    def assign(self) -> List[Assignment]:
        proba = np.array(self.weights) / 100
        assignees = np.random.choice(range(len(self.weights)), size=self.dataset_size, p=proba)
        return [Assignment(user=user, example=example) for example, user in enumerate(assignees)]
