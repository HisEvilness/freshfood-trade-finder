import streamlit as st
import json
import pandas as pd

# Load trade region data
with open("data/top_25_trade_regions.json", "r") as f:
    region_data = json.load(f)

# Convert to DataFrame for filtering
df = pd.DataFrame(region_data)

st.set_page_config(page_title="🌍 Trade Region Targeting Tool", layout="wide")
st.title("🌍 Trade Focus Finder - The Fresh Food Group")

st.markdown("""
This tool helps identify high-potential countries for B2B food export based on:
- Demand Potential
- FX Reserve Stability
- USD Readiness
- Buyer Type Focus
""")

# Sidebar filters
st.sidebar.header("🔍 Filter Criteria")
selected_demand = st.sidebar.multiselect("Demand Potential", df['Demand Potential'].unique())
selected_fx = st.sidebar.multiselect("FX Reserve Status", df['FX Reserve Status'].unique())
selected_usd = st.sidebar.selectbox("USD Readiness", ["Any", True, False])

# Filter logic
filtered_df = df.copy()
if selected_demand:
    filtered_df = filtered_df[filtered_df['Demand Potential'].isin(selected_demand)]
if selected_fx:
    filtered_df = filtered_df[filtered_df['FX Reserve Status'].isin(selected_fx)]
if selected_usd != "Any":
    filtered_df = filtered_df[filtered_df['USD Readiness'] == selected_usd]

# Display results
st.subheader("🎯 Filtered Trade Opportunities")
st.dataframe(filtered_df[["Region", "Demand Potential", "FX Reserve Status", "USD Readiness", "Buyer Type Focus"]])

# Export option
st.download_button(
    label="📥 Download Filtered List (CSV)",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_trade_targets.csv",
    mime="text/csv"
)
