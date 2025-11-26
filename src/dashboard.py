
import streamlit as st
import pandas as pd
import os
from data_processor.loading_cleaning import prepare_data


# Configuration
# Set up the page configuration
st.set_page_config(
    layout="wide",
    page_title="Toronto Bike-Sharing Analytics",
    menu_items={'About': 'Basic data loading tool for Toronto Bike Share data.'}
)


@st.cache_data
def load_and_clean_data(data_path: str) -> pd.DataFrame:
    """
    Loads and cleans the dataset by calling the US-1 tested function.
    This function runs only once until the data file or the code changes.
    """
    st.info(f"Attempting to load and clean data from: {data_path}")

    # 1. US-1: Load and Clean Data
    try:
        # Calls the successfully tested function from US-1
        df_clean = prepare_data(data_path)
        # st.success("✅ Data successfully loaded and cleaned!")
        return df_clean
    except Exception as e:
        st.error(f"❌ ERROR during data processing: {e}")
        st.stop()

    return None


def main():
    # --- UI Setup ---
    st.title("🚴 Toronto Bike-Sharing Analytics Tool")
    st.markdown("---")
    # st.header("Stage 1: Data Preparation Status (US-1 Complete)")

    # Define the data path (Adjust this path if your file is located elsewhere)
    data_file_path = os.path.join(os.getcwd(), 'data', 'bike_share_data.csv')

    # --- Load Data Pipeline ---
    try:
        # Load the cleaned data (using the cached function)
        cleaned_data = load_and_clean_data(data_file_path)
    except FileNotFoundError:
        st.error(f"Error: Data file not found at {data_file_path}. Please check the path and file name.")
        st.stop()

    # --- Display Basic Metrics ---

    if cleaned_data is not None:
        st.subheader("Cleaned Data Summary")

        # Display the total number of records after cleaning
        total_trips = len(cleaned_data)
        st.metric(label="Total Cleaned Trips", value=f"{total_trips:,}")

        # Display the first few rows of the cleaned data to confirm quality
        st.markdown("#### Preview of Cleaned Data (First 5 Rows)")
        st.dataframe(cleaned_data.head(), width='stretch')

        # Confirmation of data types (checks AC 2 from US-1)
        st.markdown("#### Data Type Confirmation")
        # Display only the critical columns to check for datetime conversion
        try:
            st.dataframe(cleaned_data[['Start Time', 'End Time']].dtypes.to_frame(), width='stretch')
        except KeyError:
            st.warning("Could not find 'start_time' and 'end_time' columns for dtype check.")


if __name__ == '__main__':
    # Ensure the data directory exists before trying to access the file
    if not os.path.exists('data'):
        os.makedirs('data')
    main()