from dataclasses import dataclass
from typing import Sequence


@dataclass
class HeftLocalRank:
    task_time_s: float
    succ_comm_times_s: Sequence[float]
    succ_ranks_s: Sequence[float]


@dataclass
class HeftGlobalRank:
    local_rank_s: float
    max_deadline_s: float
    app_deadline_s: float
