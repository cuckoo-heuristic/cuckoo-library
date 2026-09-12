from typing import Sequence
from cuckoo_library.decorator.type import type_decorator
from cuckoo_library.type.communication_type import (
    LocalTaskComputeEnergy,
    LocalTaskComputeTime,
    MECTaskComputeTime,
    SolutionDistanceBound,
    V2VServiceCompileTime,
    V2VTaskComputeEnergy,
    V2VTaskProcessingTime,
    V2VTaskTotalComputeTime,
)


@type_decorator(
    dc_type=LocalTaskComputeTime,
    return_type=float,
)
def local_task_compute_time(cpu_cycles: float, local_cpu_freq_hz: float) -> float:
    """
    Name:
        Local task compute time

    Description:
        Computes local execution time of a task.

    Meaning:
        - cpu_cycles: required CPU cycles for the task
        - local_cpu_freq_hz: local CPU frequency (Hz)
    """
    C = float(cpu_cycles)
    f = float(local_cpu_freq_hz)
    if C <= 0.0 or f <= 0.0:
        return 0.0
    return float(C / f)


@type_decorator(
    dc_type=LocalTaskComputeEnergy,
    return_type=float,
)
def local_task_compute_energy(
    kappa: float, local_cpu_freq_hz: float, cpu_cycles: float
) -> float:
    """
    Name:
        Local task compute energy

    Description:
        Computes local execution energy using dynamic power model.

    Meaning:
        - kappa: effective switched capacitance coefficient
        - local_cpu_freq_hz: local CPU frequency (Hz)
        - cpu_cycles: required CPU cycles for the task
    """
    k = float(kappa)
    f = float(local_cpu_freq_hz)
    C = float(cpu_cycles)
    if k <= 0.0 or f <= 0.0 or C <= 0.0:
        return 0.0
    return float(k * (f**2) * C)


@type_decorator(
    dc_type=V2VServiceCompileTime,
    return_type=float,
)
def v2v_service_compile_time(
    v_k: Sequence[float],
    u_k_peer: Sequence[float],
    w_k_cycles: Sequence[float],
    peer_cpu_freq_hz: float,
) -> float:
    """
    Name:
        V2V service compile time

    Description:
        Computes service/environment setup time on a peer vehicle.

    Meaning:
        - v_k: service requirement flags for the task (per k)
        - u_k_peer: cached service flags on peer vehicle (per k)
        - w_k_cycles: required CPU cycles for building service k (per k)
        - peer_cpu_freq_hz: peer CPU frequency (Hz)
    """
    f = float(peer_cpu_freq_hz)
    if f <= 0.0:
        return 0.0

    if not v_k or not u_k_peer or not w_k_cycles:
        return 0.0

    K = min(len(v_k), len(u_k_peer), len(w_k_cycles))
    if K == 0:
        return 0.0

    total_cycles = 0.0
    for k in range(K):
        v = float(v_k[k])
        u = float(u_k_peer[k])
        W = float(w_k_cycles[k])

        need_build = v * (1.0 - u)
        if need_build > 0.0 and W > 0.0:
            total_cycles += need_build * W

    return float(total_cycles / f)


@type_decorator(
    dc_type=V2VTaskProcessingTime,
    return_type=float,
)
def v2v_task_processing_time(cpu_cycles: float, peer_cpu_freq_hz: float) -> float:
    """
    Name:
        V2V task processing time

    Description:
        Computes task processing time on peer vehicle.

    Meaning:
        - cpu_cycles: required CPU cycles
        - peer_cpu_freq_hz: peer CPU frequency (Hz)
    """
    C = float(cpu_cycles)
    f = float(peer_cpu_freq_hz)
    if C <= 0.0 or f <= 0.0:
        return 0.0
    return float(C / f)


@type_decorator(
    dc_type=V2VTaskTotalComputeTime,
    return_type=float,
)
def v2v_task_total_compute_time(
    compile_time_s: float, processing_time_s: float
) -> float:
    """
    Name:
        V2V total compute time

    Description:
        Computes total compute time on peer vehicle (setup + processing).

    Meaning:
        - compile_time_s: service compile/setup time
        - processing_time_s: task processing time
    """
    t1 = float(compile_time_s)
    t2 = float(processing_time_s)
    if t1 < 0.0:
        t1 = 0.0
    if t2 < 0.0:
        t2 = 0.0
    return float(t1 + t2)


@type_decorator(
    dc_type=V2VTaskComputeEnergy,
    return_type=float,
)
def v2v_task_compute_energy(
    kappa: float,
    v_k: Sequence[float],
    u_k_peer: Sequence[float],
    w_k_cycles: Sequence[float],
    peer_cpu_freq_hz: float,
    cpu_cycles: float,
) -> float:
    """
    Name:
        V2V task compute energy

    Description:
        Computes compute energy on peer vehicle (service setup + processing).

    Meaning:
        - kappa: effective switched capacitance coefficient
        - v_k: service requirement flags for the task (per k)
        - u_k_peer: cached service flags on peer vehicle (per k)
        - w_k_cycles: required CPU cycles for building service k (per k)
        - peer_cpu_freq_hz: peer CPU frequency (Hz)
        - cpu_cycles: required CPU cycles for processing the task
    """
    k = float(kappa)
    f = float(peer_cpu_freq_hz)
    C = float(cpu_cycles)

    if k <= 0.0 or f <= 0.0:
        return 0.0

    setup_cycles = 0.0
    if v_k and u_k_peer and w_k_cycles:
        K = min(len(v_k), len(u_k_peer), len(w_k_cycles))
        for i in range(K):
            v = float(v_k[i])
            u = float(u_k_peer[i])
            W = float(w_k_cycles[i])
            need_build = v * (1.0 - u)
            if need_build > 0.0 and W > 0.0:
                setup_cycles += need_build * W

    setup_energy = k * (f**2) * setup_cycles

    proc_energy = 0.0
    if C > 0.0:
        proc_energy = k * (f**2) * C

    return float(setup_energy + proc_energy)


@type_decorator(
    dc_type=MECTaskComputeTime,
    return_type=float,
)
def mec_task_compute_time(
    v_k: Sequence[float],
    u_k_mec: Sequence[float],
    w_k_cycles: Sequence[float],
    mec_cpu_freq_hz: float,
    cpu_cycles: float,
) -> float:
    """
    Name:
        MEC task compute time

    Description:
        Computes total compute time on MEC (service setup + processing).

    Meaning:
        - v_k: service requirement flags for the task (per k)
        - u_k_mec: cached service flags on MEC (per k)
        - w_k_cycles: required CPU cycles for building service k (per k)
        - mec_cpu_freq_hz: MEC CPU frequency (Hz)
        - cpu_cycles: required CPU cycles for processing the task
    """
    f = float(mec_cpu_freq_hz)
    C = float(cpu_cycles)
    if f <= 0.0:
        return 0.0

    setup_cycles = 0.0
    if v_k and u_k_mec and w_k_cycles:
        K = min(len(v_k), len(u_k_mec), len(w_k_cycles))
        for i in range(K):
            v = float(v_k[i])
            u = float(u_k_mec[i])
            W = float(w_k_cycles[i])
            need_build = v * (1.0 - u)
            if need_build > 0.0 and W > 0.0:
                setup_cycles += need_build * W

    setup_time = setup_cycles / f
    proc_time = 0.0 if C <= 0.0 else (C / f)

    return float(setup_time + proc_time)


@type_decorator(
    dc_type=SolutionDistanceBound,
    return_type=Sequence[int],
)
def solution_distance_bound(i_diff: int) -> Sequence[int]:
    """
    Name:
        Solution distance bound

    Description:
        Returns lower and upper bound of distance H based on i differences.

    Meaning:
        - i_diff: number of differing elements
    """
    i = int(i_diff)
    if i < 0:
        i = 0
    return [i, 2 * i]
