from dataclasses import dataclass
from typing import Sequence


@dataclass
class ApplicationOffloadingEfficiency:
    alpha_n: float
    beta_n: float
    t_ref_s: float
    t_off_s: float
    e_loc_j: float
    e_off_j: float


@dataclass
class ReferenceTime:
    t_loc_s: float
    t_ddl_s: float


@dataclass
class AllLocalExecutionTime:
    cpu_cycles_list: Sequence[float]
    f_max_local_hz: float


@dataclass
class AllLocalExecutionEnergy:
    kappa: float
    cpu_cycles_list: Sequence[float]
    f_max_local_hz: float


@dataclass
class OffloadedCompletionTime:
    task_finish_times_by_provider_s: Sequence[
        Sequence[float]
    ]  # per task: list of finish times per provider
    z_task_provider: Sequence[Sequence[float]]  # per task: one-hot over providers


@dataclass
class OffloadedTotalEnergy:
    compute_energy_by_provider_j: Sequence[
        Sequence[float]
    ]  # per task: list of compute energies per provider
    z_task_provider: Sequence[Sequence[float]]  # per task: one-hot over providers
