import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="🌍 Trade Region Targeting Tool", layout="wide")

# Load full dataset
with open("data/trade_regions.json", "r") as f:
    region_data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(region_data)

# Debug: show column headers to verify names
st.write("🧪 Columns in dataset:", df.columns.tolist())

# Load product-region mapping
with open("data/product_mapping.json", "r") as f:
    product_mapping = json.load(f)

# Display last updated timestamp
st.caption(f"🗓️ Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d')}")

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
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    selected_continent = st.multiselect("🌎 Region", df['Continent'].unique())
with col2:
    selected_demand = st.multiselect("📈 Demand", df['Demand Potential'].unique())
with col3:
    selected_fx = st.multiselect("💱 FX Status", df['FX Reserve Status'].unique())
with col4:
    selected_score = st.multiselect("🎯 Score", df['Score'].unique())
with col5:
    selected_product = st.selectbox("🍚 Product Focus", ["All"] + sorted(product_mapping.keys()))

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
if selected_product != "All":
    product_regions = product_mapping[selected_product]
    filtered_df = filtered_df[filtered_df['Region'].isin(product_regions)]

# Highlight rows based on score
def highlight_top(row):
    if row['Score'] == "A":
        return ['background-color: #d4edda'] * len(row)
    return [''] * len(row)

# Display Table
st.subheader("📊 Filtered Regional Market Opportunities")

try:
    display_columns = [col for col in ["Region", "Continent", "Demand Potential", "FX Reserve Status", "USD Readiness", "Buyer Type Focus", "Score"] if col in filtered_df.columns]
    st.dataframe(
        filtered_df[display_columns].style.apply(highlight_top, axis=1),
        use_container_width=True
    )
except KeyError as e:
    st.error(f"❌ One or more columns not found: {e}")

# Export
st.download_button(
    label="📥 Download Filtered List (CSV)",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_trade_regions.csv",
    mime="text/csv"
)
