# app.py

import streamlit as st
from src.data_loader import load_and_clean_data
from src.rider_categorization import categorize_riders, filter_by_rider_type

# -----------------------------
# Load & prepare data
# -----------------------------
st.title("Toronto Bike Share – Rider Type Dashboard")

st.write("Loading data...")
clean_df = load_and_clean_data()
df_with_rider_type = categorize_riders(clean_df)

st.success("Data loaded successfully!")

# -----------------------------
# Rider Type Filter (US-4.7)
# -----------------------------
rider_choice = st.radio(
    "Select rider type:",
    options=["All", "Annual member", "Casual"],
    index=0
)

if rider_choice == "All":
    df_for_charts = df_with_rider_type
else:
    df_for_charts = filter_by_rider_type(df_with_rider_type, rider_choice)

st.write(f"### Showing {len(df_for_charts)} rides for: {rider_choice}")
st.dataframe(df_for_charts.head(50))  # show first 50 rows

# -----------------------------
# Example chart (only if column exists)
# -----------------------------
if "trip_duration" in df_for_charts.columns:
    st.write("### Trip duration distribution")
    st.bar_chart(df_for_charts["trip_duration"])
else:
    st.info("Add a duration column chart here once you know the column name.")
