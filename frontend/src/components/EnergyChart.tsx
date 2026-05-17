import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
} from "recharts";
import type { EnergyEstimate } from "../api";

const COLORS = ["#6366f1", "#f59e0b", "#10b981", "#3b82f6", "#ef4444"];

interface Props {
  data: EnergyEstimate[];
  metric: "kwh_per_tx" | "kwh_per_year";
  label: string;
}

export default function EnergyChart({ data, metric, label }: Props) {
  const sorted = [...data].sort((a, b) => a[metric] - b[metric]);
  return (
    <div style={{ width: "100%", height: 300 }}>
      <h3 style={{ textAlign: "center", marginBottom: 8 }}>{label}</h3>
      <ResponsiveContainer>
        <BarChart data={sorted} margin={{ bottom: 20 }}>
          <XAxis dataKey="chain" />
          <YAxis scale="log" domain={["auto", "auto"]} tickFormatter={(v) => v.toExponential(1)} />
          <Tooltip formatter={(v: number) => v.toExponential(4)} />
          <Bar dataKey={metric}>
            {sorted.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
