import streamlit as st
import os
import numpy as np
from datetime import time, timedelta, date
from src.data_processor.loading_cleaning import prepare_data
from src.data_processor.rider_categorization import categorize_riders, filter_by_rider_type
from src.analytics.usage_patterns import calculate_daily_rides
from src.analytics.plotting import plot_daily_rides, plot_duration_histogram
from src.data_processor.feature_engineering import label_rush_hour, calculate_trip_metrics
from src.config import URL, DATA_FILE_PATH, USER_TYPE_COL, DURATION_MIN_COL, START_TIME_COL, IS_RUSH_HOUR_COL
from src.data_processor.utils import filter_data_advanced
from src.analytics.plot_top_stations import plot_top_stations
from src.analytics.stations import get_top_starting_stations
import altair as alt

# -------------------------------------------
# STREAMLIT PAGE CONFIG
# -------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="Toronto Bike-Sharing Analytics",
    menu_items={'About': 'Basic data loading tool for Toronto Bike Share data.'}
)

# -------------------------------------------
# MAIN DASHBOARD
# -------------------------------------------
def main():

    # TITLE
    st.title("🚴 Toronto Bike-Sharing Analytics Tool")
    st.markdown("---")

    # --------------------------------------------------------
    # US-9: FULL DATA PIPELINE — RUN ONCE
    # --------------------------------------------------------
    cleaned_data = prepare_data(URL)
    df = categorize_riders(cleaned_data)
    df = label_rush_hour(df)
    df = calculate_trip_metrics(df)

    # --------------------------------------------------------
    # US-9: SUMMARY METRICS (under title)
    # --------------------------------------------------------
    total_rides = len(df)
    total_rides_fmt = f"{total_rides:,}"

    avg_duration = df[DURATION_MIN_COL].mean()
    avg_duration_fmt = f"{avg_duration:.1f}"

    subscriber_count = (df["rider_type"] == "Annual member").sum()
    subscriber_rate = (subscriber_count / total_rides) * 100
    subscriber_rate_fmt = f"{subscriber_rate:.1f}%"

    c1, c2, c3 = st.columns(3)
    with c1:  st.metric("Total Rides", total_rides_fmt)
    with c2:  st.metric("Avg Trip Duration (min)", avg_duration_fmt)
    with c3:  st.metric("Subscriber Rate", subscriber_rate_fmt)

    st.markdown("---")

    # --------------------------------------------------------
    # SIDEBAR FILTERS
    # --------------------------------------------------------
    st.sidebar.header("Filters")

    all_rider_types = sorted(df[USER_TYPE_COL].unique())
    rider_choice = st.sidebar.selectbox("Select Rider Type:", ["All"] + all_rider_types)

    df_filtered = df.copy()

    if rider_choice != "All":
        df_filtered = filter_by_rider_type(df_filtered, rider_choice)

    rush_options = ["All"] + [str(x) for x in sorted(df_filtered[IS_RUSH_HOUR_COL].unique())]
    rush_choice = st.sidebar.selectbox("Select Rush Hour:", rush_options)

    if rush_choice != "All":
        df_filtered = df_filtered[df_filtered[IS_RUSH_HOUR_COL] == (rush_choice == "True")]

    # --------------------------------------------------------
    # US-7 ADVANCED FILTERING
    # --------------------------------------------------------
    st.sidebar.markdown("---")

    max_duration = int(df[DURATION_MIN_COL].max()) + 1
    duration_range = st.sidebar.slider(
        "Trip Duration Range (minutes)",
        0, max_duration, (0, max_duration)
    )

    min_date = df_filtered[START_TIME_COL].min().date()
    max_date = df_filtered[START_TIME_COL].max().date()

    st.sidebar.subheader("📅 Date Range Filter")
    d1, d2 = st.sidebar.columns(2)
    date_start = d1.date_input("Start Date", min_date)
    date_end = d2.date_input("End Date", max_date)

    st.sidebar.subheader("🕒 Time Range Filter")
    t1, t2 = st.sidebar.columns(2)
    time_start = t1.time_input("Start Time", value=time(0, 0))
    time_end = t2.time_input("End Time", value=time(23, 59))

    df_filtered = filter_data_advanced(
        df=df_filtered,
        start_time_range=(time_start, time_end),
        min_duration=float(duration_range[0]),
        max_duration=float(duration_range[1]),
        start_date=date_start,
        end_date=date_end
    )

    # --------------------------------------------------------
    # DISPLAY TABLE + DAILY RIDERSHIP CHART
    # --------------------------------------------------------
    left, right = st.columns(2)

    with left:
        st.write(f"### Showing {len(df_filtered)} rides for: {rider_choice}")
        st.dataframe(df_filtered.head(10))

    with right:
        daily_rides = calculate_daily_rides(df_filtered)
        st.plotly_chart(plot_daily_rides(daily_rides), use_container_width=True)

    # --------------------------------------------------------
    # US-8 FULL-WIDTH TRIP DURATION CHART (FIXED)
    # --------------------------------------------------------
    st.markdown("---")
    st.subheader("Trip Duration Comparison by Rider Type (US-8)")

    st.plotly_chart(
        plot_duration_histogram(df_filtered),
        use_container_width=True
    )

    # --------------------------------------------------------
    # TOP STARTING STATIONS
    # --------------------------------------------------------
    st.markdown("---")
    st.header("Top Starting Stations")

    top_n = st.slider("Select number of stations:", 3, 20, 10)
    top_df = get_top_starting_stations(df_filtered, top_n)
    st.altair_chart(plot_top_stations(top_df, f"Top {top_n} Busiest Stations"), use_container_width=True)
    st.dataframe(top_df)

# -------------------------------------------
# MAIN
# -------------------------------------------
if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")
    main()
