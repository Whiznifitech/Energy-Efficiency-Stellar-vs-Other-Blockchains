"""Run all collectors and write snapshots to data/snapshots.json."""
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from collectors import bitcoin, cardano, ethereum, solana, stellar

DATA_DIR = Path("data")


def run() -> list[dict]:
    DATA_DIR.mkdir(exist_ok=True)
    collectors = [stellar, bitcoin, ethereum, solana, cardano]
    results = []
    for mod in collectors:
        try:
            snapshot = mod.collect()
            results.append(asdict(snapshot))
            print(f"[ok] {snapshot.chain}")
        except Exception as exc:  # noqa: BLE001
            print(f"[error] {mod.__name__}: {exc}", file=sys.stderr)

    out = DATA_DIR / "snapshots.json"
    out.write_text(json.dumps(results, default=str, indent=2))
    print(f"\nWrote {len(results)} snapshots → {out}")
    return results


if __name__ == "__main__":
    run()
