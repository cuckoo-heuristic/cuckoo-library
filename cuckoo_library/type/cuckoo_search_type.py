from dataclasses import dataclass
from typing import Sequence


@dataclass
class CSPositionUpdate:
    x_t: Sequence[float]
    omega: float
    levy_step: Sequence[float]


@dataclass
class CSExploitationMove:
    x_t: Sequence[int]
    levy_length: int


@dataclass
class CSRandomWalkMove:
    x_t: Sequence[int]
    levy_length: int
