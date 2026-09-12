from typing import Sequence

from cuckoo_library.decorator.type import type_decorator
from cuckoo_library.type.policy_type import (
    CacheKeepStateRule,
    CacheServiceValueScore,
    SingleTaskEfficiency,
)


@type_decorator(
    dc_type=SingleTaskEfficiency,
    return_type=float,
)
def single_task_efficiency(
    alpha_n: float,
    beta_n: float,
    t_ref_s: float,
    task_finish_time_s: float,
    e_loc_j: float,
    e_task_off_j: float,
) -> float:
    """
    Name:
        Single task efficiency

    Description:
        Computes efficiency contribution of a single task executed on a selected provider.

    Meaning:
        - alpha_n: time weight
        - beta_n: energy weight
        - t_ref_s: reference time
        - task_finish_time_s: finish time of the task on provider x
        - e_loc_j: all-local energy baseline
        - e_task_off_j: offloaded energy attributed to this task/provider
    """
    a = float(alpha_n)
    b = float(beta_n)
    t_ref = float(t_ref_s)
    t_fin = float(task_finish_time_s)
    e_loc = float(e_loc_j)
    e_off = float(e_task_off_j)

    if t_ref <= 0.0 or e_loc <= 0.0:
        return 0.0

    time_gain = (t_ref - t_fin) / t_ref
    energy_gain = (e_loc - e_off) / e_loc

    return float(a * time_gain + b * energy_gain)


@type_decorator(
    dc_type=CacheKeepStateRule,
    return_type=Sequence[int],
)
def cache_keep_state_rule(U_prev: Sequence[int]) -> Sequence[int]:
    """
    Name:
        Cache keep state rule

    Description:
        Returns the previous cache state unchanged.

    Meaning:
        - U_prev: previous cache state vector
    """
    if U_prev is None:
        return []
    return list(U_prev)


@type_decorator(
    dc_type=CacheServiceValueScore,
    return_type=float,
)
def cache_service_value_score(
    cpu_cycles_list: Sequence[float],
    v_kj_list: Sequence[float],
    mu_kj: float,
    denom_cpu_cycles_list: Sequence[float],
    denom_v_kj_list: Sequence[float],
) -> float:
    """
    Name:
        Cache service value score

    Description:
        Computes value score used for cache update (knapsack value).

    Meaning:
        - cpu_cycles_list: CPU cycles of tasks in psi
        - v_kj_list: requirement flags for service k_j for tasks in psi
        - mu_kj: update counter/weight for service k_j
        - denom_cpu_cycles_list: CPU cycles in denominator aggregation
        - denom_v_kj_list: requirement flags in denominator aggregation
    """
    if not cpu_cycles_list or not v_kj_list:
        return 0.0

    n1 = min(len(cpu_cycles_list), len(v_kj_list))
    numer = 0.0
    for i in range(n1):
        numer += float(cpu_cycles_list[i]) * float(v_kj_list[i])

    if not denom_cpu_cycles_list or not denom_v_kj_list:
        return 0.0

    n2 = min(len(denom_cpu_cycles_list), len(denom_v_kj_list))
    denom_sum = 0.0
    for i in range(n2):
        denom_sum += float(denom_cpu_cycles_list[i]) * float(denom_v_kj_list[i])

    denom = (float(mu_kj) + 1.0) * denom_sum
    if denom <= 0.0:
        return 0.0

    return float(numer / denom)
