from dataclasses import dataclass
from typing import Sequence


@dataclass
class CacheStateUpdateConstraint:
    u_prev_k: float
    z_task_rank: float
    v_task_requires_k: float


@dataclass
class CacheCapacityConstraint:
    u_k: Sequence[float]
    L_k: Sequence[float]
    L_max: float


@dataclass
class CacheCapacityUsed:
    u_k: Sequence[float]
    L_k: Sequence[float]
