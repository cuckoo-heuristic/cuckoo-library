from cuckoo_library.algorithm.levy_flight import (
    levy_length_random_walk,
    levy_length_to_best,
    levy_step_mantegna,
)


def test_levy_step_mantegna():
    assert levy_step_mantegna(8.0, 4.0, 2.0) == 4.0
    assert levy_step_mantegna(1.0, 0.0, 2.0) == 0.0


def test_levy_length_to_best():
    assert levy_length_to_best(2.0, 1.25) == 5


def test_levy_length_random_walk():
    assert levy_length_random_walk(2.0, 1.25) == 5
