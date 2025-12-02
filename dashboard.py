
import streamlit as st
import os
from src.data_processor.loading_cleaning import prepare_data
from src.data_processor.rider_categorization import categorize_riders, filter_by_rider_type
from src.analytics.usage_patterns import calculate_daily_rides
from src.analytics.plotting import plot_daily_rides
from src.data_processor.feature_engineering import label_rush_hour,calculate_trip_metrics


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

    # Define the data path (Adjust this path if your file is located elsewhere)
    data_file_path = os.path.join(os.getcwd(), 'data', 'bike_share_data.csv')

    # --- Load Data Pipeline ---
    try:
        # Calls the successfully tested function from US-1
        cleaned_data = prepare_data(data_file_path)
        # st.success("✅ Data successfully loaded and cleaned!")
    except Exception as e:
        st.error(f"❌ ERROR during data processing: {e}")
        st.error(f"Error: Data file not found at {data_file_path}. Please check the path and file name.")
        st.stop()

    # --- Display Basic Metrics ---

    if cleaned_data is not None:
        # -------------------------------------------
        # Categorize riders
        # -------------------------------------------
        df_with_rider_type = categorize_riders(cleaned_data)

        ## Calculate columns trip duration and distance US-2
        label_rush_hour(df_with_rider_type)
        calculate_trip_metrics(df_with_rider_type)

        st.sidebar.header("Filters")

        # -------------------------------------------
        # Rider Type Selectbox (Dynamic)
        # -------------------------------------------
        all_rider_types = sorted(df_with_rider_type["User Type"].unique())
        options = ["All"] + all_rider_types

        rider_choice = st.sidebar.selectbox(
            "Select Rider Type:",
            options=options,
            index=0
        )

        # -------------------------------------------
        # Apply your exact filtering logic
        # -------------------------------------------
        df_for_charts = df_with_rider_type.copy()

        if rider_choice != "All":
            df_for_charts = filter_by_rider_type(df_for_charts, rider_choice)

        # -------------------------------------------
        # Display
        # -------------------------------------------
        st.write(f"### Showing {len(df_for_charts)} rides for: {rider_choice}")
        st.dataframe(df_for_charts.head(10))

        # -------------------------------------------
        # Display the figure with all the rides accordingly to type of user
        # -------------------------------------------

        daily_rides = calculate_daily_rides(df_for_charts)
        fig = plot_daily_rides(daily_rides)
        st.plotly_chart(fig, use_container_width=False)



if __name__ == '__main__':
    # Ensure the data directory exists before trying to access the file
    if not os.path.exists('data'):
        os.makedirs('data')
    main()