from dataclasses import dataclass
from typing import Sequence


@dataclass
class SubproblemCpuFrequency:
    q_values: Sequence[float]


@dataclass
class AssignedCpuFrequency:
    z_selected: float
    f_star_local_hz: float
    f_max_provider_hz: float


@dataclass
class SubproblemTxPower:
    q_values: Sequence[float]


@dataclass
class TxPowerAuxFunction:
    z_selected: float
    alpha_n: float
    beta_n: float
    t_ref_s: float
    e_loc_j: float
    p_w: float
    h: float
    noise_delta2: float


@dataclass
class TxPowerAuxAtZero:
    z_selected: float
    alpha_n: float
    t_ref_s: float
    h: float
    noise_delta2: float


@dataclass
class SubproblemSchedulingCaching:
    q_values: Sequence[float]
