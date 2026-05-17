import { useEffect, useState } from "react";
import { fetchEstimates, triggerRefresh, type EnergyEstimate } from "./api";
import EnergyChart from "./components/EnergyChart";

export default function App() {
  const [estimates, setEstimates] = useState<EnergyEstimate[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const load = () =>
    fetchEstimates()
      .then(setEstimates)
      .catch((e) => setError(e.message));

  useEffect(() => { load(); }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    try { await triggerRefresh(); await load(); }
    catch (e: unknown) { setError((e as Error).message); }
    finally { setRefreshing(false); }
  };

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>⚡ Blockchain Energy Efficiency</h1>
      <p style={{ color: "#6b7280" }}>
        Comparing Stellar, Bitcoin, Ethereum, Solana, and Cardano using a unified methodology.
      </p>

      <button onClick={handleRefresh} disabled={refreshing} style={{ marginBottom: "1.5rem" }}>
        {refreshing ? "Refreshing…" : "Refresh data"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {estimates.length === 0 && !error && <p>No data yet — click Refresh data.</p>}

      {estimates.length > 0 && (
        <>
          <EnergyChart data={estimates} metric="kwh_per_tx" label="kWh per Transaction (log scale)" />
          <EnergyChart data={estimates} metric="kwh_per_year" label="kWh per Year — total network (log scale)" />

          <h2>Raw estimates</h2>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
            <thead>
              <tr style={{ borderBottom: "2px solid #e5e7eb" }}>
                {["Chain", "kWh/tx", "kWh/year", "gCO₂/tx", "Methodology"].map((h) => (
                  <th key={h} style={{ textAlign: "left", padding: "6px 8px" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {estimates.map((r) => (
                <tr key={r.chain} style={{ borderBottom: "1px solid #f3f4f6" }}>
                  <td style={{ padding: "6px 8px", fontWeight: 600 }}>{r.chain}</td>
                  <td style={{ padding: "6px 8px" }}>{r.kwh_per_tx.toExponential(4)}</td>
                  <td style={{ padding: "6px 8px" }}>{r.kwh_per_year.toLocaleString()}</td>
                  <td style={{ padding: "6px 8px" }}>{r.gco2_per_tx ?? "—"}</td>
                  <td style={{ padding: "6px 8px", color: "#6b7280", fontSize: 12 }}>{r.methodology}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </main>
  );
}
