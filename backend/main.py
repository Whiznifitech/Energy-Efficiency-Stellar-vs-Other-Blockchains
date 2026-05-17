"""
FastAPI backend — serves energy estimates to the frontend.

Endpoints:
  GET /api/estimates        → latest estimates for all chains
  GET /api/estimates/{chain} → single chain estimate
  POST /api/refresh         → re-run collectors + estimators

Run:
  uvicorn backend.main:app --reload
"""
import json
import subprocess
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import EnergyEstimate

app = FastAPI(title="Blockchain Energy Efficiency API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

DATA_PATH = Path("data/estimates.json")


def _load_estimates() -> list[dict]:
    if not DATA_PATH.exists():
        return []
    return json.loads(DATA_PATH.read_text())


@app.get("/api/estimates", response_model=list[EnergyEstimate])
def get_estimates():
    data = _load_estimates()
    if not data:
        raise HTTPException(status_code=404, detail="No estimates found. Run /api/refresh first.")
    return data


@app.get("/api/estimates/{chain}", response_model=EnergyEstimate)
def get_estimate(chain: str):
    data = _load_estimates()
    match = next((r for r in data if r["chain"] == chain.lower()), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"No estimate for chain '{chain}'")
    return match


@app.post("/api/refresh", status_code=202)
def refresh():
    """Re-run the full collector + estimator pipeline."""
    try:
        subprocess.run(
            [sys.executable, "-m", "collectors.run_all"],
            check=True, capture_output=True, text=True,
        )
        subprocess.run(
            [sys.executable, "-m", "estimators.run_all"],
            check=True, capture_output=True, text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise HTTPException(status_code=500, detail=exc.stderr) from exc
    return {"status": "ok"}
