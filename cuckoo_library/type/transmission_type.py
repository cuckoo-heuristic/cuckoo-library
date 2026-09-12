from dataclasses import dataclass
from typing import Sequence


@dataclass
class Distance3DInput:
    x_m: float
    y_m: float
    h_m: float
    x_n: float
    y_n: float
    h_n: float


@dataclass
class Distance2DInput:
    x_m: float
    y_m: float
    x_n: float
    y_n: float


@dataclass
class Distance1DInput:
    x_m: float
    x_n: float


@dataclass
class SpeedVehicle:
    path_len_m: float
    sim_time_s: float


@dataclass
class CurrentPosition:
    total_sim_time_s: float
    now_time_s: float
    path_xy: Sequence[Sequence[float]]


@dataclass
class PathLength:
    path_xy: Sequence[Sequence[float]]


@dataclass
class ChannelGainV2I:
    tau_nm: float
    rho: float
    varpi_nm: float
    distance_nm: float
    pathloss_exponent_gamma: float


@dataclass
class V2IUplinkRate:
    B_hz: float
    V_m: float
    tx_power_pn: float
    channel_gain_gnm: float
    noise_power_delta2: float


@dataclass
class IntermediateDataTxTime:
    data_bits: float
    link_rate_bps: float


@dataclass
class IntermediateDataTxEnergy:
    tx_power_w: float
    tx_time_s: float
