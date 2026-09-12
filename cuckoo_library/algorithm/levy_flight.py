from cuckoo_library.decorator.type import type_decorator
from cuckoo_library.type.levy_flight_type import (
    LevyLengthRandomWalk,
    LevyLengthToBest,
    LevyStepMantegna,
)


@type_decorator(
    dc_type=LevyStepMantegna,
    return_type=float,
)
def levy_step_mantegna(u: float, v: float, lambda_param: float) -> float:
    """
    Name:
        Levy step (Mantegna)

    Description:
        Generates Levy step value using Mantegna's method.

    Meaning:
        - u: Gaussian random variable
        - v: Gaussian random variable
        - lambda_param: Levy distribution parameter (1 < lambda <= 3 typically)
    """
    lam = float(lambda_param)
    if lam <= 0.0:
        return 0.0

    uu = float(u)
    vv = float(v)
    if vv == 0.0:
        return 0.0

    return float(uu / (abs(vv) ** (1.0 / lam)))


@type_decorator(
    dc_type=LevyLengthToBest,
    return_type=int,
)
def levy_length_to_best(hamming_distance: float, N_levy: float) -> int:
    """
    Name:
        Levy flight length to best

    Description:
        Computes quantized Levy flight length toward best solution.

    Meaning:
        - hamming_distance: H_m(current, best)
        - N_levy: Levy step scalar
    """
    hm = float(hamming_distance)
    nlevy = float(N_levy)
    length = 2.0 * hm * nlevy
    return int(round(length))


@type_decorator(
    dc_type=LevyLengthRandomWalk,
    return_type=int,
)
def levy_length_random_walk(I: float, N_levy: float) -> int:
    """
    Name:
        Levy flight length (random walk)

    Description:
        Computes quantized Levy flight length for random walk.

    Meaning:
        - I: random variable in the paper
        - N_levy: Levy step scalar
    """
    ii = float(I)
    nlevy = float(N_levy)
    length = 2.0 * ii * nlevy
    return int(round(length))
