"""
Solana collector — fetches validator count and TPS from the Solana RPC.

Data source: https://api.mainnet-beta.solana.com (public RPC)
Reference: Solana Foundation Energy Impact Report (CCRI, 2022)
  - ~509 W per validator (measured at wall socket)
  - ~3,400 active validators at time of study

TODO (complexity: trivial):
  - Make RPC_URL configurable via environment variable for private RPC endpoints

TODO (complexity: medium):
  - Separate vote transactions from user transactions in TPS calculation
    (Solana vote txs inflate raw TPS significantly)
"""
from datetime import datetime, timezone

import requests

from models import ChainSnapshot

RPC_URL = "https://api.mainnet-beta.solana.com"


def collect() -> ChainSnapshot:
    stats = _fetch_stats()
    return ChainSnapshot(
        chain="solana",
        timestamp=datetime.now(timezone.utc),
        tx_count_24h=stats["tx_count_24h"],
        tps_avg=stats["tps_avg"],
        node_count=stats["validator_count"],
    )


def _fetch_stats() -> dict:
    """
    TODO: call getVoteAccounts for validator count and
    getRecentPerformanceSamples for TPS.
    """
    payload = {"jsonrpc": "2.0", "id": 1, "method": "getVoteAccounts"}
    resp = requests.post(RPC_URL, json=payload, timeout=10)
    resp.raise_for_status()
    # TODO: parse resp.json()["result"]["current"] length for active validators
    return {
        "validator_count": 1_700,   # placeholder
        "tx_count_24h": 50_000_000, # placeholder (includes vote txs)
        "tps_avg": 578.0,           # placeholder non-vote TPS
    }
