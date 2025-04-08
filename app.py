import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="🌍 Trade Region Targeting Tool", layout="wide")

# Load full dataset
with open("data/trade_region.json", "r") as f:
    region_data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(region_data)

st.title("🌍 Target Regions Dashboard - The Fresh Food Group")

st.markdown("""
Identify the best regions for food exports based on:
- Demand Potential
- FX Reserve Risk
- USD Payment Ease
- Buyer Type
- Overall Strategic Score (A–C)
""")

# Column Filters
col1, col2, col3, col4 = st.columns(4)
with col1:
    selected_continent = st.multiselect("🌎 Region", df['Continent'].unique())
with col2:
    selected_demand = st.multiselect("📈 Demand", df['Demand Potential'].unique())
with col3:
    selected_fx = st.multiselect("💱 FX Status", df['FX Reserve Status'].unique())
with col4:
    selected_score = st.multiselect("🎯 Score", df['Score'].unique())

# Filter Logic
filtered_df = df.copy()
if selected_continent:
    filtered_df = filtered_df[filtered_df['Continent'].isin(selected_continent)]
if selected_demand:
    filtered_df = filtered_df[filtered_df['Demand Potential'].isin(selected_demand)]
if selected_fx:
    filtered_df = filtered_df[filtered_df['FX Reserve Status'].isin(selected_fx)]
if selected_score:
    filtered_df = filtered_df[filtered_df['Score'].isin(selected_score)]

# Display Table
st.subheader("📊 Filtered Regional Market Opportunities")
st.dataframe(
    filtered_df[["Region", "Continent", "Demand Potential", "FX Reserve Status", "USD Readiness", "Buyer Type Focus", "Score"]],
    use_container_width=True
)

# Export
st.download_button(
    label="📥 Download Filtered List (CSV)",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_trade_regions.csv",
    mime="text/csv"
)
