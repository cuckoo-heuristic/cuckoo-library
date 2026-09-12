import math

from cuckoo_library.model.offloading_efficiency import (
    all_local_execution_energy,
    all_local_execution_time,
    application_offloading_efficiency,
    offloaded_completion_time,
    offloaded_total_energy,
    reference_time,
)


def test_reference_time_uses_smaller_positive_time():
    assert reference_time(3, 5) == 3.0
    assert reference_time(0, 5) == 5.0


def test_all_local_execution_time():
    assert all_local_execution_time([10, 20, -5], 5) == 6.0


def test_all_local_execution_energy():
    assert all_local_execution_energy(2, [10, 20, -5], 5) == 1500.0


def test_offloaded_completion_time_selects_provider_and_takes_max():
    assert offloaded_completion_time([[2, 8], [9, 3]], [[1, 0], [0, 1]]) == 3.0


def test_offloaded_total_energy_sums_selected_provider_energy():
    assert offloaded_total_energy([[2, 8], [9, 3]], [[1, 0], [0, 1]]) == 5.0


def test_application_offloading_efficiency():
    actual = application_offloading_efficiency(0.5, 0.5, 10, 8, 20, 10)
    assert math.isclose(actual, 0.35)
