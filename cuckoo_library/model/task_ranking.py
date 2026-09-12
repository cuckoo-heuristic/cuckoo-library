from typing import Sequence
from cuckoo_library.decorator.type import type_decorator
from cuckoo_library.type.task_ranking_type import HeftGlobalRank, HeftLocalRank


@type_decorator(
    dc_type=HeftLocalRank,
    return_type=float,
)
def heft_task_local_rank(
    task_time_s: float,
    succ_comm_times_s: Sequence[float],
    succ_ranks_s: Sequence[float],
) -> float:
    """
    Name:
        HEFT local rank

    Description:
        Computes HEFT-style upward rank for a task.

    Meaning:
        - task_time_s: task computation time term
        - succ_comm_times_s: communication times to each successor
        - succ_ranks_s: precomputed ranks of each successor
    """
    t = float(task_time_s)
    if not succ_comm_times_s or not succ_ranks_s:
        return float(t)

    n = min(len(succ_comm_times_s), len(succ_ranks_s))
    best = 0.0
    for i in range(n):
        best = max(best, float(succ_comm_times_s[i]) + float(succ_ranks_s[i]))
    return float(t + best)


@type_decorator(
    dc_type=HeftGlobalRank,
    return_type=float,
)
def heft_task_global_rank(
    local_rank_s: float, max_deadline_s: float, app_deadline_s: float
) -> float:
    """
    Name:
        HEFT global rank

    Description:
        Computes global rank by shifting local rank according to application deadline.

    Meaning:
        - local_rank_s: HEFT local rank
        - max_deadline_s: maximum deadline among applications
        - app_deadline_s: deadline of the current application
    """
    return float(float(local_rank_s) + float(max_deadline_s) - float(app_deadline_s))
