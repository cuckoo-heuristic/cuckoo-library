from cuckoo_library.decorator.type import type_decorator
from typing import Sequence
from cuckoo_library.type.scheduling_type import (
    AllDependenciesReceiveTime,
    DependencyOutputReceiveTime,
    ProviderRankFinishTime,
    TaskFinishTimestamp,
    TaskOffloadDecision,
    TaskStartTimestamp,
)


@type_decorator(
    dc_type=TaskOffloadDecision,
    return_type=float,
)
def task_offload_decision(
    x_id: int, is_local: bool, is_v2v: bool, is_v2i: bool
) -> float:
    """
    Name:
        Task offload decision variable

    Description:
        Encodes which service provider (local / V2V / V2I) is selected.

    Meaning:
        - x_id: selected provider identifier
        - is_local: True if local execution is selected
        - is_v2v: True if V2V peer execution is selected
        - is_v2i: True if V2I MEC execution is selected
    """
    # This is a structural decision variable in the paper.
    # Here we return 1.0 if the decision is valid, else 0.0.
    flags = int(bool(is_local)) + int(bool(is_v2v)) + int(bool(is_v2i))
    return 1.0 if flags == 1 else 0.0


@type_decorator(
    dc_type=DependencyOutputReceiveTime,
    return_type=float,
)
def dependency_output_receive_time(
    finish_time_src_s: float,
    finish_time_same_provider_s: float,
    idle_time_s: float,
    transfer_time_s: float,
    same_provider: bool,
) -> float:
    """
    Name:
        Dependency output receive time

    Description:
        Computes when the destination provider receives a predecessor output.

    Meaning:
        - finish_time_src_s: predecessor finish time at source provider
        - finish_time_same_provider_s: predecessor finish time (if same provider)
        - idle_time_s: destination provider idle time
        - transfer_time_s: data transfer time between providers
        - same_provider: True if source and destination are the same
    """
    if bool(same_provider):
        return float(finish_time_same_provider_s)

    base = max(float(finish_time_src_s), float(idle_time_s))
    t = float(transfer_time_s)
    if t < 0.0:
        t = 0.0
    return float(base + t)


@type_decorator(
    dc_type=TaskFinishTimestamp,
    return_type=float,
)
def task_finish_timestamp(start_time_s: float, compute_time_s: float) -> float:
    """
    Name:
        Task finish timestamp

    Description:
        Computes finish time of a task on a provider.

    Meaning:
        - start_time_s: task start time
        - compute_time_s: task compute time
    """
    s = float(start_time_s)
    c = float(compute_time_s)
    if c < 0.0:
        c = 0.0
    return float(s + c)


@type_decorator(
    dc_type=AllDependenciesReceiveTime,
    return_type=float,
)
def all_dependencies_receive_time(dep_receive_times_s: Sequence[float]) -> float:
    """
    Name:
        All dependencies receive time

    Description:
        Computes the time when all predecessor outputs are received (max over predecessors).

    Meaning:
        - dep_receive_times_s: receive times for each predecessor
    """
    if not dep_receive_times_s:
        return 0.0
    return float(max(float(t) for t in dep_receive_times_s))


@type_decorator(
    dc_type=TaskStartTimestamp,
    return_type=float,
)
def task_start_timestamp(
    deps_ready_time_s: float, prev_rank_finish_time_s: float
) -> float:
    """
    Name:
        Task start timestamp

    Description:
        Computes task start time considering dependencies and provider queue (rank order).

    Meaning:
        - deps_ready_time_s: time when all dependencies are ready
        - prev_rank_finish_time_s: finish time of previous ranked task on the provider
    """
    return float(max(float(deps_ready_time_s), float(prev_rank_finish_time_s)))


@type_decorator(
    dc_type=ProviderRankFinishTime,
    return_type=float,
)
def provider_rank_finish_time(
    task_finish_times_s: Sequence[float], z_task_to_rank: Sequence[float]
) -> float:
    """
    Name:
        Provider rank finish time

    Description:
        Aggregates finish time for a specific rank using selection indicators.

    Meaning:
        - task_finish_times_s: finish time per (candidate) task
        - z_task_to_rank: selection indicator per task (should be 0/1), sum should be 1 for valid rank
    """
    if not task_finish_times_s or not z_task_to_rank:
        return 0.0

    n = min(len(task_finish_times_s), len(z_task_to_rank))
    total = 0.0
    for i in range(n):
        total += float(z_task_to_rank[i]) * float(task_finish_times_s[i])
    return float(total)
