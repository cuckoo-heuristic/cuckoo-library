from dataclasses import dataclass
from typing import Sequence


@dataclass
class TaskOffloadDecision:
    x_id: int
    is_local: bool
    is_v2v: bool
    is_v2i: bool


@dataclass
class DependencyOutputReceiveTime:
    finish_time_src_s: float
    finish_time_same_provider_s: float
    idle_time_s: float
    transfer_time_s: float
    same_provider: bool


@dataclass
class TaskFinishTimestamp:
    start_time_s: float
    compute_time_s: float


@dataclass
class AllDependenciesReceiveTime:
    dep_receive_times_s: Sequence[float]


@dataclass
class TaskStartTimestamp:
    deps_ready_time_s: float
    prev_rank_finish_time_s: float


@dataclass
class ProviderRankFinishTime:
    task_finish_times_s: Sequence[float]
    z_task_to_rank: Sequence[float]
