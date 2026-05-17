# Methodology

## Overview

This project uses two complementary models, chosen based on each chain's consensus mechanism:

| Model | Chains | Rationale |
|---|---|---|
| Bottom-up (CCRI-style) | Stellar, Ethereum, Solana, Cardano | Node count and hardware specs are observable; no mining arms race |
| Top-down (CBECI-style) | Bitcoin | Hashrate is the primary observable; hardware mix must be inferred |

---

## Bottom-Up Model (PoS / FBA Chains)

**Formula:**

```
total_watts  = node_count × watts_per_node × PUE
kwh_per_year = total_watts × 8,760 / 1,000
kwh_per_tx   = (total_watts / 1,000) / tps_avg / 3,600
```

**Parameters:**

| Chain | watts_per_node | PUE | Source |
|---|---|---|---|
| Stellar | 186 W | 1.0 | SDF / Lund University (2021) |
| Ethereum | 100 W (blended) | 1.2 | CCRI Ethereum PoS Report (2022) |
| Solana | 509 W | 1.2 | Solana Foundation / CCRI (Sept 2022) |
| Cardano | 15 W | 1.1 | CCRI Cardano Report |

**PUE (Power Usage Effectiveness):** ratio of total facility power to IT equipment power.
A PUE of 1.0 means no overhead (e.g., home nodes with no dedicated cooling).
Data-centre nodes typically have PUE 1.1–1.6.

**Why Stellar's PUE is 1.0:** The 2021 Lund study found that ~94% of Stellar's energy
is consumed by network traffic (message-passing for SCP rounds), not compute or cooling.
Most validators run on standard servers without dedicated cooling infrastructure.

---

## Top-Down Model (Bitcoin / PoW)

**Formula:**

```
total_watts  = hashrate_TH_s × efficiency_J_per_TH
kwh_per_year = total_watts × 8,760 / 1,000
kwh_per_tx   = (total_watts / 1,000) / tps_avg / 3,600
```

**Parameters:**

| Parameter | Value | Notes |
|---|---|---|
| efficiency_J_per_TH | 25 J/TH | Mid-2024 weighted fleet average |
| Lower bound | 18 J/TH | Best-in-class ASICs only |
| Upper bound | 40 J/TH | Older hardware still in operation |

This mirrors the Cambridge CBECI approach. The efficiency parameter represents
the weighted average of the active ASIC fleet, where newer (more efficient) hardware
is weighted more heavily.

---

## Carbon Intensity

Carbon intensity (gCO₂eq/kWh) is sourced from the Electricity Maps API using
a representative grid zone per chain. This is multiplied by kWh/tx to produce gCO₂/tx.

**Limitation:** This uses a single zone per chain. A more accurate model would weight
by the geographic distribution of nodes/hashrate. See the open issue for this improvement.

---

## Known Limitations

1. **TPS denominator problem:** kWh/tx conflates network load with consensus overhead.
   A chain processing 1 tx/s vs 1,000 tx/s on the same hardware will show very different
   kWh/tx values. We report both kWh/tx and kWh/year to give full context.

2. **Stellar SCP is architecturally distinct:** SCP (Federated Byzantine Agreement) has
   no mining and no staking. Its energy use is dominated by network message-passing, not
   computation. The bottom-up model captures this correctly, but direct comparisons with
   PoW chains should be interpreted carefully.

3. **Hardware parameters are point-in-time estimates.** Node hardware evolves. Parameters
   should be updated as new studies are published.

---

## References

- CCRI Methodology Report (2022): https://carbon-ratings.com
- Cambridge CBECI: https://ccaf.io/cbnsi/cbeci
- SDF / Lund University Stellar Energy Study (2021): https://stellar.org/blog/stellar-energy-use
- Solana Foundation Energy Impact Report (2022): https://solana.com/environment
- arXiv:2109.03667 — Energy Footprint of Blockchain Consensus Mechanisms Beyond PoW
