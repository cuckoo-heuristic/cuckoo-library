from cuckoo_library.model.policy import (
    cache_keep_state_rule,
    cache_service_value_score,
    single_task_efficiency,
)


def test_single_task_efficiency():
    assert single_task_efficiency(0.5, 0.5, 10, 8, 20, 10) == 0.35


def test_cache_keep_state_rule_copies_state():
    state = [1, 0]
    result = cache_keep_state_rule(state)
    assert result == state
    assert result is not state


def test_cache_service_value_score():
    assert cache_service_value_score([10, 20], [1, 0], 1, [5, 5], [1, 1]) == 10.0 / 20.0
