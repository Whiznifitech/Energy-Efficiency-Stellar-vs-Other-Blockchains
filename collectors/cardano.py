"""
Cardano collector — fetches stake pool count and transaction data via Blockfrost.

Data source: https://blockfrost.io (requires free API key)
Reference: CCRI Cardano report — ~250 tCO₂e/year, ~0.000547 kWh/tx

TODO (complexity: trivial):
  - Load BLOCKFROST_PROJECT_ID from environment (already in .env.example)

TODO (complexity: medium):
  - Distinguish active stake pools from registered-but-inactive pools
    (only active pools contribute to energy consumption)
"""
import os
from datetime import datetime, timezone

import requests

from models import ChainSnapshot

BLOCKFROST_URL = "https://cardano-mainnet.blockfrost.io/api/v0"


def collect() -> ChainSnapshot:
    stats = _fetch_stats()
    return ChainSnapshot(
        chain="cardano",
        timestamp=datetime.now(timezone.utc),
        tx_count_24h=stats["tx_count_24h"],
        tps_avg=stats["tps_avg"],
        node_count=stats["pool_count"],
        extra={"active_pool_count": stats["pool_count"]},
    )


def _fetch_stats() -> dict:
    """
    TODO: use Blockfrost /epochs/latest/parameters for pool count
    and /blocks/latest for recent tx throughput.
    Requires BLOCKFROST_PROJECT_ID env var.
    """
    project_id = os.getenv("BLOCKFROST_PROJECT_ID", "")
    if not project_id:
        # Return placeholder so pipeline runs without credentials
        return {"pool_count": 3_000, "tx_count_24h": 70_000, "tps_avg": 0.81}

    headers = {"project_id": project_id}
    resp = requests.get(f"{BLOCKFROST_URL}/epochs/latest", headers=headers, timeout=10)
    resp.raise_for_status()
    # TODO: parse resp.json() for active_stake_pool_count
    return {"pool_count": 3_000, "tx_count_24h": 70_000, "tps_avg": 0.81}
