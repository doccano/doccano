import abc
import dataclasses
import enum
import random
from typing import List

import numpy as np


@dataclasses.dataclass
class Assignment:
    user: int
    example: int


class StrategyName(enum.Enum):
    weighted_sequential = enum.auto()
    weighted_random = enum.auto()
    sampling_without_replacement = enum.auto()


def create_assignment_strategy(strategy_name: StrategyName, dataset_size: int, weights: List[int]) -> "BaseStrategy":
    if strategy_name == StrategyName.weighted_sequential:
        return WeightedSequentialStrategy(dataset_size, weights)
    elif strategy_name == StrategyName.weighted_random:
        return WeightedRandomStrategy(dataset_size, weights)
    elif strategy_name == StrategyName.sampling_without_replacement:
        return SamplingWithoutReplacementStrategy(dataset_size, weights)
    else:
        raise ValueError(f"Unknown strategy name: {strategy_name}")


class BaseStrategy(abc.ABC):
    @abc.abstractmethod
    def assign(self) -> List[Assignment]:
        ...


class WeightedSequentialStrategy(BaseStrategy):
    def __init__(self, dataset_size: int, weights: List[int]):
        if sum(weights) != 100:
            raise ValueError("Sum of weights must be 100")
        self.dataset_size = dataset_size
        self.weights = weights

    def assign(self) -> List[Assignment]:
        assignments = []
        cumsum = np.cumsum([0] + self.weights)
        ratio = np.round(cumsum / 100 * self.dataset_size).astype(int)
        for user, (start, end) in enumerate(zip(ratio, ratio[1:])):  # Todo: use itertools.pairwise
            assignments.extend([Assignment(user=user, example=example) for example in range(start, end)])
        return assignments


class WeightedRandomStrategy(BaseStrategy):
    def __init__(self, dataset_size: int, weights: List[int]):
        if sum(weights) != 100:
            raise ValueError("Sum of weights must be 100")
        self.dataset_size = dataset_size
        self.weights = weights

    def assign(self) -> List[Assignment]:
        proba = np.array(self.weights) / 100
        assignees = np.random.choice(range(len(self.weights)), size=self.dataset_size, p=proba)
        return [Assignment(user=user, example=example) for example, user in enumerate(assignees)]


class SamplingWithoutReplacementStrategy(BaseStrategy):
    def __init__(self, dataset_size: int, weights: List[int]):
        if not (0 <= sum(weights) <= 100 * len(weights)):
            raise ValueError("Sum of weights must be between 0 and 100 x number of members")
        self.dataset_size = dataset_size
        self.weights = weights

    def assign(self) -> List[Assignment]:
        assignments = []
        proba = np.array(self.weights) / 100
        for user, p in enumerate(proba):
            count = int(self.dataset_size * p)
            examples = random.sample(range(self.dataset_size), count)
            assignments.extend([Assignment(user=user, example=example) for example in examples])
        return assignments
