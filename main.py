import pandas as pd

# run_data_check.py
import os
import pandas as pd
from src.data_processor.loading_cleaning import prepare_data


# 1. Define the actual path to your data file
# IMPORTANT: Adjust this path if your file is named differently or located elsewhere
DATA_FILE_PATH = os.path.join(os.getcwd(), 'data', 'bike_share_data.csv')


def run_data_pipeline():
    print(f"--- Starting data processing for: {DATA_FILE_PATH} ---")
    # In src/data_processor/loading_cleaning.py, inside prepare_data(data_source)

    # 1. Load the data
    df = pd.read_csv(DATA_FILE_PATH)

    # ------------------ TEMPORARY DEBUG CODE START ------------------
    print("\n--- DEBUG: ACTUAL COLUMNS LOADED ---")
    print(df.columns.tolist())
    print(df.isnull().sum())
    print("--------------------------------------\n")
    # ------------------ TEMPORARY DEBUG CODE END --------------------

    # 2. Convert to datetime objects
    # ... rest of your code ...

    # Load and clean the real data
    try:
        df_clean = prepare_data(DATA_FILE_PATH)
        print("\nSUCCESS: prepare_data function executed.")
        return df_clean
    except FileNotFoundError as e:
        print(f"\nERROR: Could not find the file. {e}")
        return None


if __name__ == '__main__':
    clean_data = run_data_pipeline()

    if clean_data is not None:
        print("\n--- Validation Checks ---")
        # Go to Step 3 for the remaining checks

        # (Add this section to the 'if clean_data is not None:' block in run_data_check.py)

        # 1. Check for Nulls in Critical Columns
        critical_columns = ['Trip Id', 'Trip  Duration', 'Start Station Id', 'Start Time','End Station Id',
                                   'End Time','Start Station Name', 'End Station Name','Bike Id','User Type','Model']
        null_counts = clean_data[critical_columns].isnull().sum()

        print("\n1. Null Counts in Critical Columns:")
        print(null_counts)
        # Expected Output: All counts should be 0 (Zero)

        # 2. Check Data Types
        print("\n2. Data Types Check:")
        # We only need to see the relevant columns
        print(clean_data[['Start Time', 'End Time']].info())
        # Expected Output: The 'Dtype' for both should be datetime64[ns]

        # 3. Check for Minimum Duration (must be > 60 seconds)
        min_duration = clean_data['Trip  Duration'].min()
        print(f"\n3. Minimum Trip Duration (seconds): {min_duration}")
        # Expected Output: The number must be greater than 60

        print("\n--- Validation Complete. Data is ready for US-2. ---")