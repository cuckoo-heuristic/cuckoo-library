import math
from cuckoo_library.decorator.type import type_decorator
from cuckoo_library.type.block_coordinate_descent_type import (
    AssignedCpuFrequency,
    TxPowerAuxAtZero,
    TxPowerAuxFunction,
)


@type_decorator(
    dc_type=AssignedCpuFrequency,
    return_type=float,
)
def assigned_cpu_frequency(
    z_selected: float, f_star_local_hz: float, f_max_provider_hz: float
) -> float:
    """
    Name:
        Assigned CPU frequency

    Description:
        Computes the sub-optimal assigned CPU frequency used in the paper.

    Meaning:
        - z_selected: selection indicator (0/1) for executing on this provider
        - f_star_local_hz: optimal local frequency baseline (or f*_n)
        - f_max_provider_hz: provider max CPU frequency
    """
    z = float(z_selected)
    if z <= 0.0:
        return 0.0
    return float(min(z * float(f_star_local_hz), float(f_max_provider_hz)))


@type_decorator(
    dc_type=TxPowerAuxFunction,
    return_type=float,
)
def tx_power_aux_function(
    z_selected: float,
    alpha_n: float,
    beta_n: float,
    t_ref_s: float,
    e_loc_j: float,
    p_w: float,
    h: float,
    noise_delta2: float,
) -> float:
    """
    Name:
        TX power auxiliary function

    Description:
        Helper function used for quasi-concavity-based power optimization.

    Meaning:
        - z_selected: selection indicator (0/1)
        - alpha_n, beta_n: weights
        - t_ref_s: reference time
        - e_loc_j: all-local energy
        - p_w: transmit power (W)
        - h: channel coefficient used in the paper's auxiliary form
        - noise_delta2: noise power
    """
    z = float(z_selected)
    if z <= 0.0:
        return 0.0

    t_ref = float(t_ref_s)
    e_loc = float(e_loc_j)
    if t_ref <= 0.0 or e_loc <= 0.0:
        return 0.0

    p = float(p_w)
    hh = float(h)
    d2 = float(noise_delta2)
    if hh <= 0.0 or d2 <= 0.0 or p < 0.0:
        return 0.0

    term_log = math.log2(1.0 + (p * hh) / d2)
    denom = math.log(2.0) * (d2 + p * hh)

    left = z * (float(beta_n) / e_loc) * term_log
    right = z * ((float(alpha_n) / t_ref) + (float(beta_n) / e_loc) * p) * (hh / denom)

    return float(left - right)


@type_decorator(
    dc_type=TxPowerAuxFunction,
    return_type=float,
)
def tx_power_aux_derivative(
    z_selected: float,
    alpha_n: float,
    beta_n: float,
    t_ref_s: float,
    e_loc_j: float,
    p_w: float,
    h: float,
    noise_delta2: float,
) -> float:
    """
    Name:
        TX power auxiliary derivative

    Description:
        Derivative of the auxiliary function w.r.t transmit power.

    Meaning:
        - same as tx_power_aux_function inputs
    """
    z = float(z_selected)
    if z <= 0.0:
        return 0.0

    t_ref = float(t_ref_s)
    e_loc = float(e_loc_j)
    if t_ref <= 0.0 or e_loc <= 0.0:
        return 0.0

    p = float(p_w)
    hh = float(h)
    d2 = float(noise_delta2)
    if hh <= 0.0 or d2 <= 0.0 or p < 0.0:
        return 0.0

    numer = z * (hh**2) * ((float(alpha_n) / t_ref) + (float(beta_n) / e_loc) * p)
    denom = math.log(2.0) * ((d2 + p * hh) ** 2)

    return float(numer / denom)


@type_decorator(
    dc_type=TxPowerAuxAtZero,
    return_type=float,
)
def tx_power_aux_at_zero(
    z_selected: float, alpha_n: float, t_ref_s: float, h: float, noise_delta2: float
) -> float:
    """
    Name:
        TX power auxiliary at zero

    Description:
        Auxiliary function value at p=0 (used in the paper's reasoning).

    Meaning:
        - z_selected: selection indicator (0/1)
        - alpha_n: time weight
        - t_ref_s: reference time
        - h: channel coefficient
        - noise_delta2: noise power
    """
    z = float(z_selected)
    if z <= 0.0:
        return 0.0

    t_ref = float(t_ref_s)
    hh = float(h)
    d2 = float(noise_delta2)
    if t_ref <= 0.0 or hh <= 0.0 or d2 <= 0.0:
        return 0.0

    return float(-(z * float(alpha_n) * hh) / (math.log(2.0) * d2 * t_ref))
