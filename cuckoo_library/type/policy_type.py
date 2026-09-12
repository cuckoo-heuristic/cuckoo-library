from dataclasses import dataclass
from typing import Sequence


@dataclass
class SingleTaskEfficiency:
    alpha_n: float
    beta_n: float
    t_ref_s: float
    task_finish_time_s: float
    e_loc_j: float
    e_task_off_j: float


@dataclass
class CacheKeepStateRule:
    U_prev: Sequence[int]


@dataclass
class CacheServiceValueScore:
    cpu_cycles_list: Sequence[float]  # C_{n,i} over tasks in psi
    v_kj_list: Sequence[float]  # v^{k_j}_{n,i} over tasks in psi (0/1)
    mu_kj: float
    denom_cpu_cycles_list: Sequence[float]  # cycles for denominator set
    denom_v_kj_list: Sequence[float]  # v^{k_j}_{n,i} for denominator set
