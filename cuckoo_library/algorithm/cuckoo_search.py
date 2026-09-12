from typing import Sequence
from cuckoo_library.decorator.type import type_decorator
from cuckoo_library.type.cuckoo_search_type import (
    CSExploitationMove,
    CSExploitationMove,
    CSPositionUpdate,
    CSPositionUpdate,
    CSRandomWalkMove,
)


@type_decorator(
    dc_type=CSPositionUpdate,
    return_type=Sequence[float],
)
def cs_position_update(
    x_t: Sequence[float], omega: float, levy_step: Sequence[float]
) -> Sequence[float]:
    """
    Name:
        Cuckoo position update

    Description:
        Updates solution position using Levy flight step.

    Meaning:
        - x_t: current solution vector
        - omega: step scaling factor
        - levy_step: Levy step vector
    """
    if not x_t or not levy_step:
        return list(x_t) if x_t else []

    n = min(len(x_t), len(levy_step))
    w = float(omega)

    x_next = []
    for i in range(n):
        x_next.append(float(x_t[i]) + w * float(levy_step[i]))

    if len(x_t) > n:
        x_next.extend(float(v) for v in x_t[n:])

    return x_next


@type_decorator(
    dc_type=CSExploitationMove,
    return_type=Sequence[int],
)
def cs_exploitation_move(x_t: Sequence[int], levy_length: int) -> Sequence[int]:
    """
    Name:
        CS exploitation move

    Description:
        Moves solution by applying levy_length steps (abstracted as index flips).

    Meaning:
        - x_t: current binary/int solution vector
        - levy_length: number of modification steps
    """
    if not x_t:
        return []

    L = int(levy_length)
    if L <= 0:
        return list(x_t)

    x_next = list(x_t)
    n = len(x_next)

    # deterministic pseudo-move: flip first L positions (bounded)
    for i in range(min(L, n)):
        x_next[i] = 1 - int(x_next[i]) if int(x_next[i]) in (0, 1) else int(x_next[i])

    return x_next


@type_decorator(
    dc_type=CSRandomWalkMove,
    return_type=Sequence[int],
)
def cs_random_walk_move(x_t: Sequence[int], levy_length: int) -> Sequence[int]:
    """
    Name:
        CS random walk move

    Description:
        Applies a random-walk style modification to the solution.

    Meaning:
        - x_t: current binary/int solution vector
        - levy_length: number of modification steps
    """
    if not x_t:
        return []

    L = int(levy_length)
    if L <= 0:
        return list(x_t)

    x_next = list(x_t)
    n = len(x_next)

    # deterministic pseudo-walk: flip last L positions (bounded)
    for idx in range(1, min(L, n) + 1):
        i = n - idx
        x_next[i] = 1 - int(x_next[i]) if int(x_next[i]) in (0, 1) else int(x_next[i])

    return x_next
