
import streamlit as st
import os
import numpy as np
from datetime import time, timedelta,date
from src.data_processor.loading_cleaning import prepare_data
from src.data_processor.rider_categorization import categorize_riders, filter_by_rider_type
from src.analytics.usage_patterns import calculate_daily_rides
from src.analytics.plotting import plot_daily_rides
from src.data_processor.feature_engineering import label_rush_hour,calculate_trip_metrics
from src.config import DATA_FILE_PATH,USER_TYPE_COL, DURATION_MIN_COL,START_TIME_COL
from src.data_processor.utils import filter_data_advanced

# Configuration
# Set up the page configuration
st.set_page_config(
    layout="wide",
    page_title="Toronto Bike-Sharing Analytics",
    menu_items={'About': 'Basic data loading tool for Toronto Bike Share data.'}
)

def main():
    # --- UI Setup ---
    st.title("🚴 Toronto Bike-Sharing Analytics Tool")
    st.markdown("---")
    # st.header("Stage 1: Data Preparation Status (US-1 Complete)")


    # --- Load Data Pipeline ---
    try:
        # Calls the successfully tested function from US-1
        cleaned_data = prepare_data(DATA_FILE_PATH)
        # st.success("✅ Data successfully loaded and cleaned!")
    except Exception as e:
        st.error(f"❌ ERROR during data processing: {e}")
        st.error(f"Error: Data file not found at {DATA_FILE_PATH}. Please check the path and file name.")
        st.stop()

    # --- Display Basic Metrics ---

    if cleaned_data is not None:
        # -------------------------------------------
        # Categorize riders
        # -------------------------------------------
        df_with_rider_type = categorize_riders(cleaned_data)

        ## Calculate columns trip duration and distance US-2
        df_with_rider_type = label_rush_hour(df_with_rider_type)
        df_with_rider_type = calculate_trip_metrics(df_with_rider_type)

        st.sidebar.header("Filters")

        # -------------------------------------------
        # Rider Type Selectbox (Dynamic)
        # -------------------------------------------
        all_rider_types = sorted(df_with_rider_type[USER_TYPE_COL].unique())
        options = ["All"] + all_rider_types

        rider_choice = st.sidebar.selectbox(
            "Select Rider Type:",
            options=options,
            index=0
        )

        # -------------------------------------------
        # START OF FILTER CHAINING
        # -------------------------------------------
        df_for_charts = df_with_rider_type.copy()

        if rider_choice != "All":
            df_for_charts = filter_by_rider_type(df_for_charts, rider_choice)

        rush_options = sorted(df_for_charts["is_rush_hour"].unique())
        # Convert bool to string for presentation
        rush_options = [str(x) for x in rush_options]
        rush_options.insert(0, "All")

        rush_hour_choice = st.sidebar.selectbox(
            "Select Rush Hour:",
            options=rush_options,
            index=0
        )


        if rush_hour_choice != "All":
            target_bool = True if rush_hour_choice == 'True' else False
            df_for_charts = df_for_charts[df_for_charts["is_rush_hour"] == target_bool]

        # -------------------------------------------
        # 2. US-7: Advanced Filtering UI
        # -------------------------------------------
        st.sidebar.markdown("---")

        # 1. Duration Slider
        max_duration = int(df_with_rider_type[DURATION_MIN_COL].max()) + 1
        duration_range = st.sidebar.slider(
            'Trip Duration Range (minutes)',
            min_value=0,
            max_value=max_duration,
            value=(0, max_duration),
            key='main_duration_filter'
        )

        # 1. Find the absolute min and max date in the data
        min_data_date = df_for_charts[START_TIME_COL].min().date()  # Extracts the earliest date
        max_data_date = df_for_charts[START_TIME_COL].max().date()  # Extracts the latest date

        st.sidebar.subheader("📅 Date Range Filter")

        # Create two columns within the sidebar for the date inputs
        date_col1, date_col2 = st.sidebar.columns(2)

        # 1. Start Date Input
        start_date = date_col1.date_input(
            'Start Date',
            value=min_data_date,  # Default selection is the earliest date in the data
            min_value=min_data_date,  # Restrict selection to the earliest date
            max_value=max_data_date,  # Restrict selection up to the latest date
            key='start_date_input'
        )

        # 2. End Date Input
        end_date = date_col2.date_input(
            'End Date',
            value=max_data_date,  # Default selection is the latest date in the data
            min_value=min_data_date,  # Restrict selection down to the earliest date
            max_value=max_data_date,  # Restrict selection up to the latest date
            key='end_date_input'
        )
        # Combine the outputs into a tuple for filtering
        date_range_for_filter = (start_date, end_date)

        st.sidebar.subheader("🕒 Time Range Filter")
        col1, col2 = st.sidebar.columns(2)
        # 1. Start Time Input
        start_time = col1.time_input(
            'Start Time (HH:mm)',
            step=timedelta(minutes=1),
            value=time(7, 0),  # Default to 07:00 AM
            key='start_time_input'
        )

        # 2. End Time Input
        end_time = col2.time_input(
            'End Time (HH:mm)',
            value=time(19, 0),  # Default to 07:00 PM
            step=timedelta(minutes=1),
            key='end_time_input'
        )

        # 3. Apply US-7 Advanced Filter (Crucial Chaining Step)
        if df_for_charts.empty:
            st.warning("No rides match the current filter selection.")
            st.stop()

        # Extract the time component from the full datetime objects returned by the slider
        time_range_for_filter = (start_time, end_time)
        df_for_charts = filter_data_advanced(
            df=df_for_charts,
            # Pass the tuple of time objects directly
            start_time_range=time_range_for_filter,
            min_duration=float(duration_range[0]),
            max_duration=float(duration_range[1]),
            start_date=date_range_for_filter[0],  # Pass start date
            end_date=date_range_for_filter[1]  # Pass end date
        )



        # FINAL CHECK
        if df_for_charts.empty:
            st.error("No rides match the final filter criteria.")
            st.stop()

        # -------------------------------------------
        # Display
        # -------------------------------------------
        left_col, right_col = st.columns(2)

        with left_col:
            st.write(f"### Showing {len(df_for_charts)} rides for: {rider_choice}")
            st.dataframe(df_for_charts.head(10))

        # -------------------------------------------
        # Display the figure with all the rides accordingly to type of user
        # -------------------------------------------
        with right_col:
            daily_rides = calculate_daily_rides(df_for_charts)
            fig = plot_daily_rides(daily_rides)
            st.plotly_chart(fig, use_container_width=False)

        hist_values = np.histogram(df_for_charts[START_TIME_COL].dt.hour, bins=24, range=(0,24))[0]
        st.bar_chart(hist_values)

if __name__ == '__main__':
    # Ensure the data directory exists before trying to access the file
    if not os.path.exists('data'):
        os.makedirs('data')
    main()