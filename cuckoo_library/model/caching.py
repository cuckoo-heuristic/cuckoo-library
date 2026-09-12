from cuckoo_library.decorator.type import type_decorator
from typing import Sequence

from cuckoo_library.type.caching_type import (
    CacheCapacityConstraint,
    CacheCapacityUsed,
    CacheStateUpdateConstraint,
)


@type_decorator(
    dc_type=CacheStateUpdateConstraint,
    return_type=float,
)
def cache_state_update_constraint(
    u_prev_k: float, z_task_rank: float, v_task_requires_k: float
) -> float:
    """
    Name:
        Cache state update constraint (per k)

    Description:
        Computes the upper bound for updated cache flag u_{x,r}^k.

    Meaning:
        - u_prev_k: previous cache flag u_{x,r-1}^k
        - z_task_rank: whether the selected task is executed at rank r on provider x (0/1)
        - v_task_requires_k: whether the selected task requires service k (0/1)
    """
    return float(float(u_prev_k) + float(z_task_rank) * float(v_task_requires_k))


@type_decorator(
    dc_type=CacheCapacityUsed,
    return_type=float,
)
def cache_capacity_used(u_k: Sequence[float], L_k: Sequence[float]) -> float:
    """
    Name:
        Cache capacity used

    Description:
        Computes total cache space used.

    Meaning:
        - u_k: cache flags per service k (0/1)
        - L_k: cache size per service k
    """
    if not u_k or not L_k:
        return 0.0

    n = min(len(u_k), len(L_k))
    total = 0.0
    for i in range(n):
        total += float(u_k[i]) * float(L_k[i])
    return float(total)


@type_decorator(
    dc_type=CacheCapacityConstraint,
    return_type=float,
)
def cache_capacity_constraint(
    u_k: Sequence[float], L_k: Sequence[float], L_max: float
) -> float:
    """
    Name:
        Cache capacity constraint

    Description:
        Checks whether cache capacity is satisfied (returns 1.0 if satisfied else 0.0).

    Meaning:
        - u_k: cache flags per service k (0/1)
        - L_k: cache size per service k
        - L_max: maximum cache capacity
    """
    used = cache_capacity_used(u_k, L_k)
    return 1.0 if used <= float(L_max) else 0.0
