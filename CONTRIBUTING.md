# Contributing

Thank you for helping improve this project. All contributions are welcome.

## Issue Labels

Pick an issue that matches your experience level:

| Label | Scope |
|---|---|
| `complexity: trivial` | Data source URL updates, typo fixes, doc improvements |
| `complexity: medium` | New chain collector, model parameter tuning, new metric |
| `complexity: high` | Methodology extension, uncertainty modelling, new consensus type |

## Getting Started

```bash
git clone https://github.com/YOUR_ORG/energy-efficiency-stellar-vs-other-blockchains
cd energy-efficiency-stellar-vs-other-blockchains
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Running Tests

```bash
pytest tests/
```

## Adding a New Chain

1. Create `collectors/<chain>.py` implementing `collect() -> ChainSnapshot`
2. Create `estimators/<chain>.py` implementing `estimate(snapshot) -> EnergyResult`
3. Register both in `collectors/run_all.py` and `estimators/run_all.py`
4. Add a sample fixture in `tests/fixtures/`
5. Add unit tests in `tests/test_<chain>.py`

## Code Style

```bash
ruff check .
ruff format .
```

## Pull Request Checklist

- [ ] Tests pass (`pytest tests/`)
- [ ] Linter passes (`ruff check .`)
- [ ] New chain: sample fixture committed to `tests/fixtures/`
- [ ] Methodology change: `docs/methodology.md` updated

## License

By contributing you agree your work is released under the MIT License.
