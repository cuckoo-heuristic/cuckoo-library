from cuckoo_library.model.task_ranking import (
    heft_task_global_rank,
    heft_task_local_rank,
)


def test_heft_task_local_rank_uses_largest_successor_term():
    assert heft_task_local_rank(2, [3, 1], [4, 8]) == 11.0


def test_heft_task_global_rank_shifts_local_rank():
    assert heft_task_global_rank(5, 20, 7) == 18.0
