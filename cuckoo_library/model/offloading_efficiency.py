from typing import Sequence
from cuckoo_library.decorator.type import type_decorator
from cuckoo_library.type.offloading_efficiency_type import (
    AllLocalExecutionEnergy,
    AllLocalExecutionTime,
    AllLocalExecutionTime,
    ApplicationOffloadingEfficiency,
    OffloadedCompletionTime,
    OffloadedTotalEnergy,
    ReferenceTime,
)


@type_decorator(
    dc_type=ReferenceTime,
    return_type=float,
)
def reference_time(t_loc_s: float, t_ddl_s: float) -> float:
    """
    Name:
        Reference time

    Description:
        Computes reference time as min(local time, deadline).

    Meaning:
        - t_loc_s: all-local execution time
        - t_ddl_s: application deadline
    """
    t_loc = float(t_loc_s)
    t_ddl = float(t_ddl_s)
    if t_loc <= 0.0 and t_ddl <= 0.0:
        return 0.0
    if t_loc <= 0.0:
        return max(0.0, t_ddl)
    if t_ddl <= 0.0:
        return max(0.0, t_loc)
    return float(min(t_loc, t_ddl))


@type_decorator(
    dc_type=AllLocalExecutionTime,
    return_type=float,
)
def all_local_execution_time(
    cpu_cycles_list: Sequence[float], f_max_local_hz: float
) -> float:
    """
    Name:
        All-local execution time

    Description:
        Computes application time if all tasks run locally at max frequency.

    Meaning:
        - cpu_cycles_list: CPU cycles per task
        - f_max_local_hz: local max CPU frequency (Hz)
    """
    f = float(f_max_local_hz)
    if f <= 0.0 or not cpu_cycles_list:
        return 0.0

    total = 0.0
    for C in cpu_cycles_list:
        c = float(C)
        if c > 0.0:
            total += c / f
    return float(total)


@type_decorator(
    dc_type=AllLocalExecutionEnergy,
    return_type=float,
)
def all_local_execution_energy(
    kappa: float, cpu_cycles_list: Sequence[float], f_max_local_hz: float
) -> float:
    """
    Name:
        All-local execution energy

    Description:
        Computes application energy if all tasks run locally at max frequency.

    Meaning:
        - kappa: effective switched capacitance coefficient
        - cpu_cycles_list: CPU cycles per task
        - f_max_local_hz: local max CPU frequency (Hz)
    """
    k = float(kappa)
    f = float(f_max_local_hz)
    if k <= 0.0 or f <= 0.0 or not cpu_cycles_list:
        return 0.0

    total = 0.0
    for C in cpu_cycles_list:
        c = float(C)
        if c > 0.0:
            total += k * (f**2) * c
    return float(total)


@type_decorator(
    dc_type=OffloadedCompletionTime,
    return_type=float,
)
def offloaded_completion_time(
    task_finish_times_by_provider_s: Sequence[Sequence[float]],
    z_task_provider: Sequence[Sequence[float]],
) -> float:
    """
    Name:
        Offloaded completion time

    Description:
        Computes application completion time under offloading decisions
        as max over tasks of selected provider finish time.

    Meaning:
        - task_finish_times_by_provider_s: finish times per task per provider
        - z_task_provider: one-hot selection per task over providers
    """
    if not task_finish_times_by_provider_s or not z_task_provider:
        return 0.0

    T = min(len(task_finish_times_by_provider_s), len(z_task_provider))
    if T == 0:
        return 0.0

    selected_finish_times = []
    for i in range(T):
        times = task_finish_times_by_provider_s[i]
        z = z_task_provider[i]
        if not times or not z:
            continue
        n = min(len(times), len(z))
        sel = 0.0
        for j in range(n):
            sel += float(z[j]) * float(times[j])
        selected_finish_times.append(sel)

    if not selected_finish_times:
        return 0.0

    return float(max(selected_finish_times))


@type_decorator(
    dc_type=OffloadedTotalEnergy,
    return_type=float,
)
def offloaded_total_energy(
    compute_energy_by_provider_j: Sequence[Sequence[float]],
    z_task_provider: Sequence[Sequence[float]],
) -> float:
    """
    Name:
        Offloaded total energy (compute-only)

    Description:
        Computes total compute energy under offloading decisions
        by summing selected provider energy per task.

    Meaning:
        - compute_energy_by_provider_j: compute energies per task per provider
        - z_task_provider: one-hot selection per task over providers
    """
    if not compute_energy_by_provider_j or not z_task_provider:
        return 0.0

    T = min(len(compute_energy_by_provider_j), len(z_task_provider))
    if T == 0:
        return 0.0

    total = 0.0
    for i in range(T):
        energies = compute_energy_by_provider_j[i]
        z = z_task_provider[i]
        if not energies or not z:
            continue
        n = min(len(energies), len(z))
        for j in range(n):
            total += float(z[j]) * float(energies[j])
    return float(total)


@type_decorator(
    dc_type=ApplicationOffloadingEfficiency,
    return_type=float,
)
def application_offloading_efficiency(
    alpha_n: float,
    beta_n: float,
    t_ref_s: float,
    t_off_s: float,
    e_loc_j: float,
    e_off_j: float,
) -> float:
    """
    Name:
        Application offloading efficiency

    Description:
        Computes the weighted improvement in time and energy due to offloading.

    Meaning:
        - alpha_n: weight for time gain
        - beta_n: weight for energy gain
        - t_ref_s: reference time
        - t_off_s: offloaded completion time
        - e_loc_j: all-local energy
        - e_off_j: offloaded energy
    """
    a = float(alpha_n)
    b = float(beta_n)
    t_ref = float(t_ref_s)
    t_off = float(t_off_s)
    e_loc = float(e_loc_j)
    e_off = float(e_off_j)

    if t_ref <= 0.0 or e_loc <= 0.0:
        return 0.0

    time_gain = (t_ref - t_off) / t_ref
    energy_gain = (e_loc - e_off) / e_loc

    return float(a * time_gain + b * energy_gain)
