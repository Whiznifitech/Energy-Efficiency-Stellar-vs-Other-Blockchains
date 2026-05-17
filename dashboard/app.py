"""
Streamlit dashboard — visualises energy estimates across chains.

Run: streamlit run dashboard/app.py
"""
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = Path("data/estimates.json")

st.set_page_config(page_title="Blockchain Energy Efficiency", layout="wide")
st.title("⚡ Energy Efficiency: Stellar vs Other Blockchains")
st.caption(
    "Methodology: bottom-up (CCRI-style) for PoS/FBA chains; "
    "top-down (CBECI-style) for Bitcoin. See docs/methodology.md."
)

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
if not DATA_PATH.exists():
    st.warning(
        "No estimates found. Run the pipeline first:\n\n"
        "```\npython -m collectors.run_all\npython -m estimators.run_all\n```"
    )
    st.stop()

df = pd.DataFrame(json.loads(DATA_PATH.read_text()))
df["chain"] = df["chain"].str.capitalize()

# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("kWh per Transaction")
    fig = px.bar(
        df.sort_values("kwh_per_tx"),
        x="chain", y="kwh_per_tx",
        log_y=True,
        labels={"kwh_per_tx": "kWh / tx (log scale)", "chain": ""},
        color="chain",
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("kWh per Year (total network)")
    fig2 = px.bar(
        df.sort_values("kwh_per_year"),
        x="chain", y="kwh_per_year",
        log_y=True,
        labels={"kwh_per_year": "kWh / year (log scale)", "chain": ""},
        color="chain",
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------
# Raw table
# ---------------------------------------------------------------------------
st.subheader("Raw Estimates")
display_cols = ["chain", "kwh_per_tx", "kwh_per_year", "gco2_per_tx", "methodology"]
st.dataframe(df[[c for c in display_cols if c in df.columns]], use_container_width=True)
