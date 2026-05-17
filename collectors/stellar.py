"""
Stellar collector — fetches network stats from the Horizon public API.

Data source: https://horizon.stellar.org
Docs: https://developers.stellar.org/api/horizon

TODO (complexity: trivial):
  - Add retry logic for transient HTTP errors
  - Cache response to data/ directory

TODO (complexity: medium):
  - Pull live validator count from Stellar Beat or StellarExpert
  - Add 7-day rolling TPS average
"""
from datetime import datetime, timezone

import requests

from models import ChainSnapshot

HORIZON_URL = "https://horizon.stellar.org"


def collect() -> ChainSnapshot:
    """Return a ChainSnapshot with current Stellar network stats."""
    ledger_stats = _fetch_ledger_stats()
    return ChainSnapshot(
        chain="stellar",
        timestamp=datetime.now(timezone.utc),
        tx_count_24h=ledger_stats["tx_count_24h"],
        tps_avg=ledger_stats["tps_avg"],
        node_count=ledger_stats["node_count"],
        extra={
            "ledger_close_time_s": ledger_stats["ledger_close_time_s"],
        },
    )


def _fetch_ledger_stats() -> dict:
    """
    Fetch recent ledger data from Horizon and derive TPS.

    TODO: implement real aggregation over the last 24h of ledgers.
    Placeholder returns known baseline values from the 2021 SDF/Lund study
    so the estimator pipeline can run end-to-end before this is wired up.
    """
    # Verify the endpoint is reachable
    resp = requests.get(f"{HORIZON_URL}/ledgers?order=desc&limit=1", timeout=10)
    resp.raise_for_status()

    # TODO: aggregate tx_count over last 24h of ledger records
    # For now return the 2021 baseline so the pipeline is runnable
    return {
        "tx_count_24h": 500_000,   # placeholder — replace with real aggregation
        "tps_avg": 5.8,            # placeholder
        "node_count": 95,          # ~current validator count
        "ledger_close_time_s": 5.5,
    }
