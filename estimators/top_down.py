"""
Top-down energy model (CBECI-style) for Proof-of-Work chains.

Formula:
    total_watts = hashrate_eh_s × 1e18 / efficiency_j_per_hash
    kwh_per_year = total_watts × 8_760 / 1_000
    kwh_per_tx   = (total_watts / 1_000) / tps_avg / 3_600

The efficiency_j_per_hash parameter represents the weighted average of the
active ASIC hardware fleet. CBECI uses a basket of 100+ models; the default
here is a reasonable mid-2024 estimate.

TODO (complexity: high):
  - Build a hardware basket from public ASIC specs (model, efficiency, release date)
    and weight by estimated deployment share (newer = more deployed)
  - Add lower/upper bounds (most efficient vs least efficient plausible fleet)
"""
from dataclasses import dataclass

from models import ChainSnapshot, EnergyResult


@dataclass
class TopDownParams:
    # Weighted average efficiency of the active mining fleet (J/TH = W/TH/s)
    # Mid-2024 estimate: ~25 J/TH (range: ~18 J/TH best-case to ~40 J/TH worst-case)
    efficiency_j_per_th: float = 25.0


def estimate(snapshot: ChainSnapshot, params: TopDownParams) -> EnergyResult:
    """Compute energy metrics using the top-down hashrate model."""
    hashrate_th_s = snapshot.extra.get("hashrate_eh_s", 0) * 1e6  # EH/s → TH/s
    total_watts = hashrate_th_s * params.efficiency_j_per_th       # W = TH/s × J/TH
    kwh_per_year = total_watts * 8_760 / 1_000
    kwh_per_tx = (total_watts / 1_000) / max(snapshot.tps_avg, 1e-9) / 3_600

    return EnergyResult(
        chain=snapshot.chain,
        timestamp=snapshot.timestamp,
        kwh_per_tx=kwh_per_tx,
        kwh_per_year=kwh_per_year,
        methodology=(
            f"top-down: {snapshot.extra.get('hashrate_eh_s')} EH/s × "
            f"{params.efficiency_j_per_th} J/TH"
        ),
    )
