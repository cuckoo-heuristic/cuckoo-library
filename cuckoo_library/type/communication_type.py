from dataclasses import dataclass
from typing import Sequence


@dataclass
class LocalTaskComputeTime:
    cpu_cycles: float
    local_cpu_freq_hz: float


@dataclass
class LocalTaskComputeEnergy:
    kappa: float
    local_cpu_freq_hz: float
    cpu_cycles: float


@dataclass
class V2VServiceCompileTime:
    v_k: Sequence[float]
    u_k_peer: Sequence[float]
    w_k_cycles: Sequence[float]
    peer_cpu_freq_hz: float


@dataclass
class V2VTaskProcessingTime:
    cpu_cycles: float
    peer_cpu_freq_hz: float


@dataclass
class V2VTaskTotalComputeTime:
    compile_time_s: float
    processing_time_s: float


@dataclass
class V2VTaskComputeEnergy:
    kappa: float
    v_k: Sequence[float]
    u_k_peer: Sequence[float]
    w_k_cycles: Sequence[float]
    peer_cpu_freq_hz: float
    cpu_cycles: float


@dataclass
class MECTaskComputeTime:
    v_k: Sequence[float]
    u_k_mec: Sequence[float]
    w_k_cycles: Sequence[float]
    mec_cpu_freq_hz: float
    cpu_cycles: float


@dataclass
class SolutionDistanceBound:
    i_diff: int
