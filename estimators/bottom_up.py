"""
Bottom-up energy model (CCRI-style) for PoS and FBA chains.

Formula:
    total_watts = node_count × watts_per_node × pue
    kwh_per_year = total_watts × 8_760 / 1_000
    kwh_per_tx   = (total_watts / 1_000) / tps_avg / 3_600

Reference: CCRI Methodology Report (2022), SDF/Lund University (2021)
"""
from dataclasses import dataclass

from models import ChainSnapshot, EnergyResult


@dataclass
class BottomUpParams:
    watts_per_node: float  # average power draw per node at wall socket (W)
    pue: float = 1.2       # Power Usage Effectiveness (1.0 = perfect efficiency)


def estimate(snapshot: ChainSnapshot, params: BottomUpParams) -> EnergyResult:
    """Compute energy metrics using the bottom-up hardware model."""
    total_watts = snapshot.node_count * params.watts_per_node * params.pue
    kwh_per_year = total_watts * 8_760 / 1_000
    kwh_per_tx = (total_watts / 1_000) / max(snapshot.tps_avg, 1e-9) / 3_600

    return EnergyResult(
        chain=snapshot.chain,
        timestamp=snapshot.timestamp,
        kwh_per_tx=kwh_per_tx,
        kwh_per_year=kwh_per_year,
        methodology=(
            f"bottom-up: {snapshot.node_count} nodes × "
            f"{params.watts_per_node}W × PUE {params.pue}"
        ),
    )
