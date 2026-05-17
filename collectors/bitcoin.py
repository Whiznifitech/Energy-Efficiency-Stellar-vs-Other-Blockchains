"""
Bitcoin collector — fetches hashrate and transaction data from mempool.space.

Data source: https://mempool.space/api
Methodology: top-down (CBECI-style). Hashrate is the primary input to the
energy estimator; node_count is not used in the top-down model.

TODO (complexity: trivial):
  - Add configurable API base URL for self-hosted mempool instances

TODO (complexity: medium):
  - Pull hardware efficiency basket (ASIC model mix) from public mining pool data
  - Add geographic hashrate distribution for carbon intensity weighting
"""
from datetime import datetime, timezone

import requests

from models import ChainSnapshot

MEMPOOL_URL = "https://mempool.space/api"


def collect() -> ChainSnapshot:
    stats = _fetch_stats()
    return ChainSnapshot(
        chain="bitcoin",
        timestamp=datetime.now(timezone.utc),
        tx_count_24h=stats["tx_count_24h"],
        tps_avg=stats["tps_avg"],
        node_count=0,  # not used in top-down model
        extra={
            "hashrate_eh_s": stats["hashrate_eh_s"],
        },
    )


def _fetch_stats() -> dict:
    """
    Fetch current hashrate and mempool stats.

    TODO: implement real 24h tx aggregation from /api/v1/mining/blocks/fee-rates
    and hashrate from /api/v1/mining/hashrate/3d
    """
    resp = requests.get(f"{MEMPOOL_URL}/v1/mining/hashrate/3d", timeout=10)
    resp.raise_for_status()
    # TODO: parse resp.json() to extract current hashrate
    return {
        "hashrate_eh_s": 600.0,   # placeholder EH/s
        "tx_count_24h": 350_000,  # placeholder
        "tps_avg": 4.05,          # placeholder
    }
