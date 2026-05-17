"""
Carbon intensity lookup via Electricity Maps API.

Converts kWh/tx → gCO₂/tx using the grid carbon intensity of the region
where the majority of a chain's nodes operate.

API docs: https://static.electricitymaps.com/api/docs/index.html

TODO (complexity: trivial):
  - Cache responses to avoid hitting rate limits on repeated runs

TODO (complexity: medium):
  - Weight carbon intensity by geographic node distribution
    (e.g., use IP geolocation of known validators)
"""
import os

import requests

ELECTRICITY_MAPS_URL = "https://api.electricitymap.org/v3"

# Default zone codes per chain based on known node geography.
# These are starting-point estimates — replace with real distribution data.
DEFAULT_ZONES: dict[str, str] = {
    "stellar": "US",   # SDF nodes + community spread; US as proxy
    "bitcoin": "US",   # largest hashrate share
    "ethereum": "US",
    "solana": "US",
    "cardano": "EU",   # community-run, Europe-heavy
}


def get_carbon_intensity_g_per_kwh(zone: str) -> float | None:
    """
    Return the current carbon intensity (gCO₂eq/kWh) for a grid zone.
    Returns None if the API key is not configured or the request fails.
    """
    api_key = os.getenv("ELECTRICITY_MAPS_API_KEY", "")
    if not api_key:
        return None

    try:
        resp = requests.get(
            f"{ELECTRICITY_MAPS_URL}/carbon-intensity/latest",
            params={"zone": zone},
            headers={"auth-token": api_key},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()["carbonIntensity"]
    except Exception:  # noqa: BLE001
        return None


def annotate_carbon(chain: str, kwh_per_tx: float) -> float | None:
    """Return gCO₂/tx for a chain, or None if carbon data is unavailable."""
    zone = DEFAULT_ZONES.get(chain, "US")
    intensity = get_carbon_intensity_g_per_kwh(zone)
    if intensity is None:
        return None
    return kwh_per_tx * intensity
