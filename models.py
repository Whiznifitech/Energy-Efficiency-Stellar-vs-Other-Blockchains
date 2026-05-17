"""Shared data models used across collectors and estimators."""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ChainSnapshot:
    """Raw on-chain data captured at a point in time."""
    chain: str
    timestamp: datetime
    tx_count_24h: int
    tps_avg: float          # transactions per second (24h average)
    node_count: int
    extra: dict = field(default_factory=dict)  # chain-specific fields


@dataclass
class EnergyResult:
    """Computed energy metrics for one chain at one point in time."""
    chain: str
    timestamp: datetime
    kwh_per_tx: float
    kwh_per_year: float
    gco2_per_tx: float | None = None  # None when carbon data unavailable
    methodology: str = ""             # human-readable description of model used
