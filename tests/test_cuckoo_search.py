from cuckoo_library.algorithm.cuckoo_search import (
    cs_exploitation_move,
    cs_position_update,
    cs_random_walk_move,
)


def test_cs_position_update_preserves_unmatched_tail():
    assert cs_position_update([1, 2, 3], 0.5, [4, 6]) == [3.0, 5.0, 3.0]


def test_cs_exploitation_move_flips_first_positions():
    assert cs_exploitation_move([0, 1, 0], 2) == [1, 0, 0]


def test_cs_random_walk_move_flips_last_positions():
    assert cs_random_walk_move([0, 1, 0], 2) == [0, 0, 1]
