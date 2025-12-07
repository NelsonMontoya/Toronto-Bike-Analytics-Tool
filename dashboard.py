import streamlit as st
import os
from datetime import time, date

from src.data_processor.loading_cleaning import prepare_data
from src.data_processor.rider_categorization import categorize_riders, filter_by_rider_type
from src.data_processor.feature_engineering import label_rush_hour, calculate_trip_metrics
from src.data_processor.utils import filter_data_advanced

from src.analytics.usage_patterns import calculate_daily_rides
from src.analytics.plotting import plot_daily_rides, plot_duration_histogram
from src.analytics.stations import get_top_starting_stations
from src.analytics.plot_top_stations import plot_top_stations

from src.config import URL, USER_TYPE_COL, DURATION_MIN_COL, START_TIME_COL, IS_RUSH_HOUR_COL


# ---------------------------------------------------
# CUSTOM CSS – MODERN LONG TABS
# ---------------------------------------------------
TABS_STYLE = """
<style>
div[data-baseweb="tab-list"] {
    display: flex;
    justify-content: space-evenly;
    gap: 2rem;
    padding-bottom: 6px;
    border-bottom: 2px solid #444;
}

button[data-baseweb="tab"] {
    font-size: 18px !important;
    font-weight: 600 !important;
    padding: 14px 40px !important;
    border-radius: 10px !important;
    background-color: #222 !important;
    border: 1px solid #555 !important;
    color: #ccc !important;
    transition: all 0.2s ease-in-out !important;
}

button[data-baseweb="tab"]:hover {
    background-color: #333 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #0D6EFD !important;
    color: white !important;
    border-color: #0B5ED7 !important;
    box-shadow: 0px 2px 10px rgba(13,110,253,0.35) !important;
}
</style>
"""
st.markdown(TABS_STYLE, unsafe_allow_html=True)

# ---------------------------------------------------
# KPI CARDS – GOLD & DARK THEME
# ---------------------------------------------------
KPI_CARD_CSS = """
<style>
div[data-testid="column"] > div {
    display: flex;
    justify-content: center;
}

/* KPI CARD */
.kpi-card {
    background-color: #111 !important;
    border: 2px solid #D4AF37 !important;
    border-radius: 14px !important;
    padding: 20px 25px !important;
    width: 90% !important;
    text-align: center !important;
    box-shadow: 0px 0px 15px rgba(212,175,55,0.35);
}

/* Title */
.kpi-card-title {
    color: #D4AF37 !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    margin-bottom: 5px !important;
}

/* Value */
.kpi-card-value {
    color: white !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}
</style>
"""
st.markdown(KPI_CARD_CSS, unsafe_allow_html=True)

# ---------------------------------------------------
# GLOBAL DARK BACKGROUND
# ---------------------------------------------------
DARK_BG = """
<style>
/* Main app background */
.stApp {
    background-color: #000000 !important;
}

/* Text color default */
html, body, [class*="css"]  {
    color: #FFFFFF !important;
}

/* Remove white blocks */
.block-container {
    background-color: #000000 !important;
}

/* Fix dataframe background */
[data-testid="stDataFrame"] div {
    background-color: #000 !important;
    color: #FFF !important;
}

/* Fix code blocks if used */
.stCodeBlock {
    background-color: #111 !important;
    color: white !important;
}
</style>
"""
st.markdown(DARK_BG, unsafe_allow_html=True)

# ---------------------------------------------------
# STREAMLIT CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Toronto Bike-Sharing Analytics",
    layout="wide"
)


# ---------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------
def main():

    # --------------------------
    # TITLE
    # --------------------------
    st.title("Toronto Bike-Sharing Analytics Dashboard")
    st.markdown("Interactive analytics for Toronto Bike Share ridership.")
    st.markdown("---")

    # --------------------------
    # DATA PIPELINE
    # --------------------------
    raw = prepare_data(URL)
    df = categorize_riders(raw)
    df = label_rush_hour(df)
    df = calculate_trip_metrics(df)

    # --------------------------
    # TABS IN FINAL ORDER
    # --------------------------
    tab_timeline, tab_duration, tab_stations, tab_data = st.tabs(
        ["Timeline & KPIs", "Duration Analytics", "Stations Analytics", "Data Tables"]
    )

    # ============================================================
    # TAB 1 — TIMELINE + KPI CARDS
    # ============================================================
    with tab_timeline:

        st.subheader("Key Performance Indicators")

        total_rides = f"{len(df):,}"
        avg_duration = df[DURATION_MIN_COL].mean()
        subscriber_rate = (df["rider_type"] == "Annual member").mean() * 100

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-card-title">Total Rides</div>
                    <div class="kpi-card-value">{total_rides}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-card-title">Avg Trip Duration (min)</div>
                    <div class="kpi-card-value">{avg_duration:.1f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-card-title">Subscriber Share</div>
                    <div class="kpi-card-value">{subscriber_rate:.1f}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.subheader("Daily Ridership Timeline")

        df_timeline = df.copy()

        rider_types = ["All"] + sorted(df[USER_TYPE_COL].unique())
        rider_choice = st.selectbox("Filter by Rider Type:", rider_types)

        if rider_choice != "All":
            df_timeline = filter_by_rider_type(df_timeline, rider_choice)

        daily_rides = calculate_daily_rides(df_timeline)

        st.plotly_chart(
            plot_daily_rides(daily_rides),
            use_container_width=True
        )

    # ============================================================
    # TAB 2 — DURATION ANALYTICS
    # ============================================================
    with tab_duration:

        st.subheader("Trip Duration Analysis")

        df_duration = df.copy()

        rider_choice_a = st.selectbox(
            "Rider Type:",
            ["All"] + sorted(df[USER_TYPE_COL].unique())
        )

        if rider_choice_a != "All":
            df_duration = filter_by_rider_type(df_duration, rider_choice_a)

        st.plotly_chart(
            plot_duration_histogram(df_duration),
            use_container_width=True
        )

    # ============================================================
    # TAB 3 — STATIONS ANALYTICS
    # ============================================================
    with tab_stations:

        st.subheader("Top Starting Stations")

        top_n = st.slider("Number of Stations:", 3, 20, 10)

        top_df = get_top_starting_stations(df, top_n)

        st.altair_chart(
            plot_top_stations(top_df, f"Top {top_n} Starting Stations"),
            use_container_width=True
        )

        st.subheader("Station List")
        st.dataframe(top_df, use_container_width=True)

    # ============================================================
    # TAB 4 — DATA TABLES
    # ============================================================
    with tab_data:

        st.subheader("Dataset Explorer")

        df_filtered = df.copy()

        # Rider Type Filter
        rider_choice_d = st.selectbox(
            "Rider Type Filter:",
            ["All"] + sorted(df[USER_TYPE_COL].unique())
        )
        if rider_choice_d != "All":
            df_filtered = filter_by_rider_type(df_filtered, rider_choice_d)

        # Duration filter
        max_duration = int(df[DURATION_MIN_COL].max()) + 1
        duration_range = st.slider(
            "Trip Duration (min)",
            0, max_duration, (0, max_duration)
        )

        # Date filter
        min_date = df[START_TIME_COL].min().date()
        max_date = df[START_TIME_COL].max().date()

        col1, col2 = st.columns(2)
        date_start = col1.date_input("Start Date", min_date)
        date_end = col2.date_input("End Date", max_date)

        # Time filter
        col3, col4 = st.columns(2)
        time_start = col3.time_input("Start Time", time(0, 0))
        time_end = col4.time_input("End Time", time(23, 59))

        df_filtered = filter_data_advanced(
            df=df_filtered,
            start_time_range=(time_start, time_end),
            min_duration=float(duration_range[0]),
            max_duration=float(duration_range[1]),
            start_date=date_start,
            end_date=date_end
        )

        st.write(f"### Showing {len(df_filtered):,} filtered rides")
        st.dataframe(df_filtered, use_container_width=True)


# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------
if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")
    main()
