from datetime import datetime
from pydantic import BaseModel


class EnergyEstimate(BaseModel):
    chain: str
    timestamp: datetime
    kwh_per_tx: float
    kwh_per_year: float
    gco2_per_tx: float | None = None
    methodology: str = ""
