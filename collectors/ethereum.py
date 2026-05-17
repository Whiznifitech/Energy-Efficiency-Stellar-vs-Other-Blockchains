"""
Ethereum collector — fetches validator count and transaction data.

Data sources:
  - Beaconcha.in API: https://beaconcha.in/api/v1/docs
  - Etherscan (tx count): https://etherscan.io/apis

TODO (complexity: trivial):
  - Add ETHERSCAN_API_KEY to .env.example and load here

TODO (complexity: medium):
  - Distinguish home staker vs professional vs cloud validator mix
    (CCRI uses ~3 node classes with different power draws and PUEs)
"""
from datetime import datetime, timezone

import requests

from models import ChainSnapshot

BEACONCHAIN_URL = "https://beaconcha.in/api/v1"


def collect() -> ChainSnapshot:
    stats = _fetch_stats()
    return ChainSnapshot(
        chain="ethereum",
        timestamp=datetime.now(timezone.utc),
        tx_count_24h=stats["tx_count_24h"],
        tps_avg=stats["tps_avg"],
        node_count=stats["validator_count"],
        extra={
            "validator_count": stats["validator_count"],
        },
    )


def _fetch_stats() -> dict:
    """
    TODO: call beaconcha.in /api/v1/epoch/latest for validator count,
    and Etherscan /api?module=proxy&action=eth_blockNumber for tx throughput.
    """
    return {
        "validator_count": 1_000_000,  # placeholder
        "tx_count_24h": 1_100_000,     # placeholder
        "tps_avg": 12.7,               # placeholder
    }
