from cuckoo_library.model.communication import (
    local_task_compute_energy,
    local_task_compute_time,
    mec_task_compute_time,
    solution_distance_bound,
    v2v_service_compile_time,
    v2v_task_compute_energy,
    v2v_task_processing_time,
    v2v_task_total_compute_time,
)


def test_local_task_compute_time():
    assert local_task_compute_time(100, 10) == 10.0
    assert local_task_compute_time(0, 10) == 0.0


def test_local_task_compute_energy():
    assert local_task_compute_energy(2, 3, 4) == 72.0


def test_v2v_service_compile_time():
    assert v2v_service_compile_time([1, 1], [0, 1], [10, 20], 5) == 2.0


def test_v2v_task_processing_time():
    assert v2v_task_processing_time(100, 20) == 5.0


def test_v2v_task_total_compute_time_clamps_negative_parts():
    assert v2v_task_total_compute_time(-1, 3) == 3.0


def test_v2v_task_compute_energy():
    assert v2v_task_compute_energy(2, [1], [0], [10], 3, 4) == 252.0


def test_mec_task_compute_time():
    assert mec_task_compute_time([1], [0], [10], 5, 20) == 6.0


def test_solution_distance_bound():
    assert solution_distance_bound(3) == [3, 6]
    assert solution_distance_bound(-1) == [0, 0]
