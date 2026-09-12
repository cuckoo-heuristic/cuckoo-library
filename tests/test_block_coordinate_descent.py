import math

from cuckoo_library.model.block_coordinate_descent import (
    assigned_cpu_frequency,
    tx_power_aux_at_zero,
    tx_power_aux_derivative,
    tx_power_aux_function,
)


def test_assigned_cpu_frequency_caps_selected_frequency():
    assert assigned_cpu_frequency(1.0, 3.0, 2.0) == 2.0
    assert assigned_cpu_frequency(0.0, 3.0, 2.0) == 0.0


def test_tx_power_aux_function_matches_formula():
    actual = tx_power_aux_function(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)
    log_term = math.log2(1.0 + 6.0 * 7.0 / 8.0)
    expected = 3.0 / 5.0 * log_term - (2.0 / 4.0 + 3.0 / 5.0 * 6.0) * 7.0 / (math.log(2.0) * (8.0 + 6.0 * 7.0))
    assert math.isclose(actual, expected)
    assert tx_power_aux_function(0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0) == 0.0


def test_tx_power_aux_derivative_matches_formula():
    actual = tx_power_aux_derivative(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)
    expected = 7.0**2 * (2.0 / 4.0 + 3.0 / 5.0 * 6.0) / (math.log(2.0) * (8.0 + 6.0 * 7.0) ** 2)
    assert math.isclose(actual, expected)


def test_tx_power_aux_at_zero_matches_formula():
    actual = tx_power_aux_at_zero(1.0, 2.0, 4.0, 7.0, 8.0)
    expected = -(2.0 * 7.0) / (math.log(2.0) * 8.0 * 4.0)
    assert math.isclose(actual, expected)
