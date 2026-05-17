"""Unit tests for energy estimators."""
import json
from datetime import datetime
from pathlib import Path


from models import ChainSnapshot
from estimators import chains as chain_estimators
from estimators.bottom_up import BottomUpParams, estimate as bottom_up

FIXTURES = json.loads(
    (Path(__file__).parent / "fixtures" / "snapshots.json").read_text()
)


def _snapshot(chain: str) -> ChainSnapshot:
    data = FIXTURES[chain].copy()
    data["timestamp"] = datetime.fromisoformat(data["timestamp"])
    return ChainSnapshot(**data)


# ---------------------------------------------------------------------------
# Bottom-up model
# ---------------------------------------------------------------------------

def test_bottom_up_stellar_kwh_per_year():
    """Stellar: 95 nodes × 186 W × PUE 1.0 → ~154 kWh/year (rough sanity check)."""
    result = chain_estimators.stellar(_snapshot("stellar"))
    expected_kwh_year = 95 * 186 * 1.0 * 8_760 / 1_000
    assert abs(result.kwh_per_year - expected_kwh_year) < 1.0


def test_bottom_up_kwh_per_tx_positive():
    for chain in ("stellar", "ethereum", "solana", "cardano"):
        result = getattr(chain_estimators, chain)(_snapshot(chain))
        assert result.kwh_per_tx > 0, f"{chain}: kwh_per_tx should be positive"


def test_bottom_up_stellar_less_than_bitcoin():
    """Stellar should consume orders of magnitude less energy per tx than Bitcoin."""
    stellar_result = chain_estimators.stellar(_snapshot("stellar"))
    bitcoin_result = chain_estimators.bitcoin(_snapshot("bitcoin"))
    assert stellar_result.kwh_per_tx < bitcoin_result.kwh_per_tx / 1_000


def test_bottom_up_zero_tps_does_not_crash():
    """A snapshot with zero TPS should not raise ZeroDivisionError."""
    snap = _snapshot("stellar")
    snap.tps_avg = 0.0
    result = bottom_up(snap, BottomUpParams(watts_per_node=186.0, pue=1.0))
    assert result.kwh_per_tx > 0


# ---------------------------------------------------------------------------
# Top-down model (Bitcoin)
# ---------------------------------------------------------------------------

def test_top_down_bitcoin_kwh_per_year_order_of_magnitude():
    """Bitcoin should be in the hundreds of TWh/year range."""
    result = chain_estimators.bitcoin(_snapshot("bitcoin"))
    # 600 EH/s × 25 J/TH = 600e6 TH/s × 25 J/TH = 15e9 W = 15 GW
    # 15 GW × 8760h / 1000 = ~131,400 GWh = ~131 TWh
    assert 50_000_000 < result.kwh_per_year < 300_000_000_000  # 50 GWh to 300 TWh


def test_top_down_methodology_string():
    result = chain_estimators.bitcoin(_snapshot("bitcoin"))
    assert "top-down" in result.methodology


# ---------------------------------------------------------------------------
# EnergyResult fields
# ---------------------------------------------------------------------------

def test_result_chain_name_preserved():
    for chain in ("stellar", "bitcoin", "ethereum", "solana", "cardano"):
        result = getattr(chain_estimators, chain)(_snapshot(chain))
        assert result.chain == chain
