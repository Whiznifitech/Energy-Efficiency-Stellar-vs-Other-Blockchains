# Energy Efficiency: Stellar vs Other Blockchains

An open-source tool for measuring and comparing the real energy consumption of major blockchain networks using a consistent, reproducible methodology.

## Why This Project

Existing energy studies are either chain-specific (SDF/PwC for Stellar, CBECI for Bitcoin) or proprietary (CCRI). No open-source tool applies a unified methodology across Stellar, Bitcoin, Ethereum, Solana, and Cardano. This project fills that gap.

## Chains Covered

| Chain    | Consensus     | Methodology          |
|----------|---------------|----------------------|
| Stellar  | SCP / FBA     | Bottom-up (CCRI-style) |
| Ethereum | PoS           | Bottom-up (CCRI-style) |
| Solana   | PoH + PoS     | Bottom-up (CCRI-style) |
| Cardano  | Ouroboros PoS | Bottom-up (CCRI-style) |
| Bitcoin  | PoW           | Top-down (CBECI-style) |

## Metrics

- **kWh/tx** — energy per transaction
- **kWh/year** — total annualised network energy
- **gCO₂/tx** — carbon intensity per transaction (via Electricity Maps)

## Methodology

**Bottom-up (PoS/FBA chains):** Node count × hardware power draw × PUE → total network watts → divide by TPS for per-tx figure. Mirrors the CCRI approach used in institutional ESG benchmarks.

**Top-down (Bitcoin):** Hashrate × hardware efficiency basket → total power. Mirrors the Cambridge CBECI model.

See [`docs/methodology.md`](docs/methodology.md) for full details.

## Project Structure

```
├── collectors/        # On-chain data fetchers (one module per chain)
├── estimators/        # Energy models (one module per chain)
├── carbon/            # Carbon intensity lookup (Electricity Maps)
├── backend/           # FastAPI REST API
├── frontend/          # React + Vite UI
├── dashboard/         # Streamlit visualisation app (alternative UI)
├── data/              # Cached snapshots (gitignored except samples)
├── docs/              # Methodology, data sources, contribution guide
└── tests/             # Unit and integration tests
```

## Quick Start

**Pipeline (data collection + estimation):**
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m collectors.run_all          # fetch latest on-chain data
python -m estimators.run_all          # compute energy estimates
```

**Backend API:**
```bash
uvicorn backend.main:app --reload     # http://localhost:8000
# API docs: http://localhost:8000/docs
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev                           # http://localhost:5173
```

**Streamlit dashboard (alternative):**
```bash
streamlit run dashboard/app.py
```

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Issues are labelled by complexity:
- `complexity: trivial` — good first issues (data source updates, doc fixes)
- `complexity: medium` — new chain integrations, model improvements
- `complexity: high` — methodology extensions, new metrics

## License

MIT
