import math

from cuckoo_library.model.transmission import (
    channel_gain_v2i,
    current_position,
    distance_1d,
    distance_2d,
    distance_3d,
    intermediate_data_tx_energy,
    intermediate_data_tx_time,
    path_length_2d,
    speed_vehicle,
    v2i_uplink_rate,
)


def test_channel_gain_v2i():
    assert channel_gain_v2i(2, 3, 4, 2, 1) == 12.0


def test_v2i_uplink_rate():
    assert math.isclose(v2i_uplink_rate(100, 2, 2, 3, 1), 100 * math.log2(7) / 2)


def test_intermediate_data_tx_time():
    assert intermediate_data_tx_time(100, 20) == 5.0


def test_intermediate_data_tx_energy():
    assert intermediate_data_tx_energy(2, 5) == 10.0


def test_distance_3d():
    assert distance_3d(0, 0, 0, 2, 3, 6) == 7.0


def test_distance_2d():
    assert distance_2d(0, 0, 3, 4) == 5.0


def test_distance_1d():
    assert distance_1d(2, 7) == 5.0


def test_speed_vehicle():
    assert speed_vehicle(100, 20) == 5.0
    assert speed_vehicle(100, 0) == 0.0


def test_current_position_interpolates_polyline_by_length():
    assert current_position(10, 5, [[0, 0], [10, 0], [10, 10]]) == (10.0, 0.0)


def test_path_length_2d():
    assert path_length_2d([[0, 0], [3, 4], [3, 8]]) == 9.0
