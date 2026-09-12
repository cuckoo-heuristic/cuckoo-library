from cuckoo_library.model.caching import (
    cache_capacity_constraint,
    cache_capacity_used,
    cache_state_update_constraint,
)


def test_cache_state_update_constraint():
    assert cache_state_update_constraint(1.0, 1.0, 0.5) == 1.5


def test_cache_capacity_used():
    assert cache_capacity_used([1, 0, 1], [2, 4, 3]) == 5.0
    assert cache_capacity_used([], [2]) == 0.0


def test_cache_capacity_constraint():
    assert cache_capacity_constraint([1, 0, 1], [2, 4, 3], 5) == 1.0
    assert cache_capacity_constraint([1, 1], [2, 4], 5) == 0.0
