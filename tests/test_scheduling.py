from cuckoo_library.model.scheduling import (
    all_dependencies_receive_time,
    dependency_output_receive_time,
    provider_rank_finish_time,
    task_finish_timestamp,
    task_offload_decision,
    task_start_timestamp,
)


def test_task_offload_decision_requires_exactly_one_provider():
    assert task_offload_decision(1, True, False, False) == 1.0
    assert task_offload_decision(1, True, True, False) == 0.0


def test_dependency_output_receive_time():
    assert dependency_output_receive_time(3, 4, 5, 2, False) == 7.0
    assert dependency_output_receive_time(3, 4, 5, 2, True) == 4.0


def test_task_finish_timestamp_clamps_negative_compute_time():
    assert task_finish_timestamp(5, -2) == 5.0


def test_all_dependencies_receive_time():
    assert all_dependencies_receive_time([2, 5, 3]) == 5.0


def test_task_start_timestamp():
    assert task_start_timestamp(4, 7) == 7.0


def test_provider_rank_finish_time():
    assert provider_rank_finish_time([4, 7], [0, 1]) == 7.0
