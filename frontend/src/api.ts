export interface EnergyEstimate {
  chain: string;
  timestamp: string;
  kwh_per_tx: number;
  kwh_per_year: number;
  gco2_per_tx: number | null;
  methodology: string;
}

const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function fetchEstimates(): Promise<EnergyEstimate[]> {
  const res = await fetch(`${BASE}/api/estimates`);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}

export async function triggerRefresh(): Promise<void> {
  const res = await fetch(`${BASE}/api/refresh`, { method: "POST" });
  if (!res.ok) throw new Error(`Refresh failed ${res.status}`);
}
