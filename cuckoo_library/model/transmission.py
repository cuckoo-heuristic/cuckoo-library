from dataclasses import dataclass
import math
from typing import Union, Callable, Any, Type, Sequence, Tuple
from cuckoo_library.decorator.type import type_decorator
from cuckoo_library.type.transmission_type import (
    ChannelGainV2I,
    CurrentPosition,
    Distance1DInput,
    Distance2DInput,
    Distance3DInput,
    IntermediateDataTxEnergy,
    IntermediateDataTxTime,
    PathLength,
    SpeedVehicle,
    V2IUplinkRate,
)


@type_decorator(
    dc_type=ChannelGainV2I,
    return_type=float,
)
def channel_gain_v2i(
    tau_nm: float,
    rho: float,
    varpi_nm: float,
    distance_nm: float,
    pathloss_exponent_gamma: float,
) -> float:
    """
    Name:
        Channel gain (V2I)

    Description:
        Computes channel gain using path-loss and fading factors.

    Meaning:
        - tau_nm: large-scale fading / shadowing factor
        - rho: channel constant
        - varpi_nm: small-scale fading factor
        - distance_nm: distance between vehicle and RSU
        - pathloss_exponent_gamma: path loss exponent
    """
    d = float(distance_nm)
    if d <= 0.0:
        return 0.0

    gamma = float(pathloss_exponent_gamma)
    return float(float(tau_nm) * float(rho) * float(varpi_nm) * (d ** (-gamma)))


@type_decorator(
    dc_type=V2IUplinkRate,
    return_type=float,
)
def v2i_uplink_rate(
    B_hz: float,
    V_m: float,
    tx_power_pn: float,
    channel_gain_gnm: float,
    noise_power_delta2: float,
) -> float:
    """
    Name:
        Uplink rate (V2I)

    Description:
        Computes uplink transmission rate from a vehicle to an RSU.

    Meaning:
        - B_hz: total bandwidth (Hz)
        - V_m: number of vehicles sharing the RSU bandwidth
        - tx_power_pn: transmit power
        - channel_gain_gnm: channel gain
        - noise_power_delta2: noise power
    """
    B = float(B_hz)
    Vm = float(V_m)
    if B <= 0.0 or Vm <= 0.0:
        return 0.0

    delta2 = float(noise_power_delta2)
    if delta2 <= 0.0:
        return 0.0

    snr = (float(tx_power_pn) * float(channel_gain_gnm)) / delta2
    if snr <= 0.0:
        return 0.0

    return float((B / Vm) * math.log2(1.0 + snr))


@type_decorator(
    dc_type=IntermediateDataTxTime,
    return_type=float,
)
def intermediate_data_tx_time(data_bits: float, link_rate_bps: float) -> float:
    """
    Name:
        Intermediate data transmission time

    Description:
        Computes transmission time for intermediate data over a given link rate.

    Meaning:
        - data_bits: data size in bits
        - link_rate_bps: link rate in bits per second
    """
    r = float(link_rate_bps)
    if r <= 0.0:
        return 0.0

    d = float(data_bits)
    if d <= 0.0:
        return 0.0

    return float(d / r)


@type_decorator(
    dc_type=IntermediateDataTxEnergy,
    return_type=float,
)
def intermediate_data_tx_energy(tx_power_w: float, tx_time_s: float) -> float:
    """
    Name:
        Intermediate data transmission energy

    Description:
        Computes energy consumption for transmitting intermediate data.

    Meaning:
        - tx_power_w: transmit power in watts
        - tx_time_s: transmission time in seconds
    """
    p = float(tx_power_w)
    t = float(tx_time_s)
    if p <= 0.0 or t <= 0.0:
        return 0.0

    return float(p * t)


@type_decorator(
    dc_type=Distance3DInput,
    return_type=float,
)
def distance_3d(
    x_m: float, y_m: float, h_m: float, x_n: float, y_n: float, h_n: float
) -> float:
    """
    Name:
        3D distance

    Description:
        Computes the 3D Euclidean distance between transmitter (n) and receiver (m).

    Meaning:
        - x_m, y_m, h_m: receiver coordinates (e.g., RSU/MEC or target vehicle)
        - x_n, y_n, h_n: transmitter coordinates (vehicle n)
    """
    dx = x_m - x_n
    dy = y_m - y_n
    dh = h_m - h_n

    return float((dx * dx + dy * dy + dh * dh) ** 0.5)


@type_decorator(
    dc_type=Distance2DInput,
    return_type=float,
)
def distance_2d(x_m: float, y_m: float, x_n: float, y_n: float) -> float:
    """
    Name:
        2D distance

    Description:
        Computes the 2D Euclidean distance between transmitter (n) and receiver (m).

    Meaning:
        - x_m, y_m: receiver coordinates (e.g., RSU/MEC or target vehicle)
        - x_n, y_n: transmitter coordinates (vehicle n)
    """
    dx = x_m - x_n
    dy = y_m - y_n

    return float((dx * dx + dy * dy) ** 0.5)


@type_decorator(
    dc_type=Distance1DInput,
    return_type=float,
)
def distance_1d(x_m: float, x_n: float) -> float:
    """
    Name:
        1D distance

    Description:
        Computes the 1D distance between transmitter (n) and receiver (m).

    Meaning:
        - x_m: receiver coordinate (e.g., RSU/MEC or target vehicle)
        - x_n: transmitter coordinate (vehicle n)
    """
    dx = x_m - x_n

    return float(abs(dx))


@type_decorator(
    dc_type=SpeedVehicle,
    return_type=float,
)
def speed_vehicle(path_len_m: float, sim_time_s: float) -> float:
    """
    Name:
        Speed (from path length & simulation time)

    Description:
        Computes average speed based on traveled path length and simulation time.

    Meaning:
        - path_len_m: traveled path length (meters)
        - sim_time_s: simulation time elapsed (seconds)

    Formula:
        v = s / t
    """
    if sim_time_s <= 0.0:
        return 0.0

    return float(path_len_m / sim_time_s)


@type_decorator(
    dc_type=CurrentPosition,
    return_type=tuple,
)
def current_position(
    total_sim_time_s: float,
    now_time_s: float,
    path_xy: Sequence[Sequence[float]],
) -> Tuple[float, float]:
    """
    Name:
        Current position (x,y)

    Description:
        Returns current (x,y) on the polyline path based on simulation time,
        assuming uniform progress along the path.

    Meaning:
        - total_sim_time_s: total simulation duration (seconds)
        - now_time_s: current time (seconds)
        - path_xy: path points as [[x,y], ...]
    """
    if not path_xy:
        raise ValueError("path_xy is empty")
    if len(path_xy) == 1 or total_sim_time_s <= 0.0:
        return float(path_xy[0][0]), float(path_xy[0][1])

    p = now_time_s / total_sim_time_s
    if p <= 0.0:
        return float(path_xy[0][0]), float(path_xy[0][1])
    if p >= 1.0:
        return float(path_xy[-1][0]), float(path_xy[-1][1])

    seg_lens = []
    total_len = 0.0
    for i in range(len(path_xy) - 1):
        x1, y1 = float(path_xy[i][0]), float(path_xy[i][1])
        x2, y2 = float(path_xy[i + 1][0]), float(path_xy[i + 1][1])
        dx, dy = x2 - x1, y2 - y1
        L = (dx * dx + dy * dy) ** 0.5
        seg_lens.append(L)
        total_len += L

    if total_len <= 0.0:
        return float(path_xy[0][0]), float(path_xy[0][1])

    d = p * total_len

    acc = 0.0
    for i, L in enumerate(seg_lens):
        if d <= acc + L or i == len(seg_lens) - 1:
            x1, y1 = float(path_xy[i][0]), float(path_xy[i][1])
            x2, y2 = float(path_xy[i + 1][0]), float(path_xy[i + 1][1])
            if L <= 0.0:
                return x1, y1
            r = (d - acc) / L
            return float(x1 + r * (x2 - x1)), float(y1 + r * (y2 - y1))
        acc += L

    return float(path_xy[-1][0]), float(path_xy[-1][1])


@type_decorator(
    dc_type=PathLength,
    return_type=float,
)
def path_length_2d(path_xy: Sequence[Sequence[float]]) -> float:
    """
    Name:
        Path length (2D)

    Description:
        Computes total length of a 2D polyline path.

    Meaning:
        - path_xy: array of [x,y] points describing the path
    """
    if not path_xy or len(path_xy) < 2:
        return 0.0

    total = 0.0
    for i in range(len(path_xy) - 1):
        x1, y1 = float(path_xy[i][0]), float(path_xy[i][1])
        x2, y2 = float(path_xy[i + 1][0]), float(path_xy[i + 1][1])
        dx = x2 - x1
        dy = y2 - y1
        total += (dx * dx + dy * dy) ** 0.5

    return float(total)
