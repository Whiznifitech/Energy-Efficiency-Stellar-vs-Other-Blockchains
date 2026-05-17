"""Load snapshots from data/ and compute energy estimates for all chains."""
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from models import ChainSnapshot
from estimators import chains as chain_estimators

DATA_DIR = Path("data")
CHAIN_FN = {
    "stellar": chain_estimators.stellar,
    "bitcoin": chain_estimators.bitcoin,
    "ethereum": chain_estimators.ethereum,
    "solana": chain_estimators.solana,
    "cardano": chain_estimators.cardano,
}


def run() -> list[dict]:
    snapshots_path = DATA_DIR / "snapshots.json"
    if not snapshots_path.exists():
        print("No snapshots found. Run collectors first.", file=sys.stderr)
        sys.exit(1)

    raw = json.loads(snapshots_path.read_text())
    results = []
    for item in raw:
        item["timestamp"] = datetime.fromisoformat(item["timestamp"])
        snapshot = ChainSnapshot(**item)
        fn = CHAIN_FN.get(snapshot.chain)
        if fn is None:
            print(f"[skip] no estimator for {snapshot.chain}", file=sys.stderr)
            continue
        result = fn(snapshot)
        results.append(asdict(result))
        print(f"[ok] {result.chain}: {result.kwh_per_tx:.6f} kWh/tx")

    out = DATA_DIR / "estimates.json"
    out.write_text(json.dumps(results, default=str, indent=2))
    print(f"\nWrote {len(results)} estimates → {out}")
    return results


if __name__ == "__main__":
    run()
