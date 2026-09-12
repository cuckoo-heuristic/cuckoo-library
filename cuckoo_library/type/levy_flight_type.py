from dataclasses import dataclass
from typing import Sequence


@dataclass
class LevyStepMantegna:
    u: float
    v: float
    lambda_param: float


@dataclass
class LevyLengthToBest:
    hamming_distance: float
    N_levy: float


@dataclass
class LevyLengthRandomWalk:
    I: float
    N_levy: float
