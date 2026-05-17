"""
Per-chain estimator wrappers.

Each function applies the correct model with chain-specific parameters.
Hardware parameters are sourced from published studies; see docs/methodology.md.

TODO (complexity: medium):
  - Load parameters from a YAML config file so contributors can tune them
    without touching Python code
"""
from models import ChainSnapshot, EnergyResult
from estimators.bottom_up import BottomUpParams, estimate as bottom_up
from estimators.top_down import TopDownParams, estimate as top_down


# ---------------------------------------------------------------------------
# Bottom-up chains (FBA / PoS)
# ---------------------------------------------------------------------------

def stellar(snapshot: ChainSnapshot) -> EnergyResult:
    """
    Parameters from SDF/Lund University (2021):
      - 132 nodes, ~186 W average per node, PUE ~1.0 (no dedicated cooling)
      - Total: ~24.6 kW → ~0.222 Wh/tx at observed TPS
    """
    return bottom_up(snapshot, BottomUpParams(watts_per_node=186.0, pue=1.0))


def ethereum(snapshot: ChainSnapshot) -> EnergyResult:
    """
    Parameters from CCRI Ethereum PoS report (2022):
      - Home staker: ~22 W; Professional: ~48 W × PUE 1.58; Cloud: ~155 W × PUE 1.15
      - Blended average used here: ~100 W × PUE 1.2
    TODO (complexity: medium): implement three-class node mix model
    """
    return bottom_up(snapshot, BottomUpParams(watts_per_node=100.0, pue=1.2))


def solana(snapshot: ChainSnapshot) -> EnergyResult:
    """
    Parameters from Solana Foundation / CCRI (Sept 2022):
      - ~509 W per validator at wall socket, PUE ~1.2
    """
    return bottom_up(snapshot, BottomUpParams(watts_per_node=509.0, pue=1.2))


def cardano(snapshot: ChainSnapshot) -> EnergyResult:
    """
    Parameters from CCRI Cardano report:
      - ~15 W per stake pool node (Raspberry Pi class hardware common)
      - PUE ~1.1
    TODO (complexity: trivial): verify current hardware baseline from community surveys
    """
    return bottom_up(snapshot, BottomUpParams(watts_per_node=15.0, pue=1.1))


# ---------------------------------------------------------------------------
# Top-down chains (PoW)
# ---------------------------------------------------------------------------

def bitcoin(snapshot: ChainSnapshot) -> EnergyResult:
    """CBECI-style top-down model. See estimators/top_down.py for details."""
    return top_down(snapshot, TopDownParams(efficiency_j_per_th=25.0))
