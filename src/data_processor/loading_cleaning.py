# Taiga Task 1.2: Implement minimal cleaning logic to pass the null count test (GREEN).
#
# Taiga Task 1.4: Implement datetime conversion logic to pass the datetime test (GREEN).


import pandas as pd
from typing import List
from src.config import (TRIP_ID_COL,TRIP_DURATION_COL,START_TIME_COL, END_TIME_COL,USER_TYPE_COL,START_STATION_COL,
                        END_STATION_COL,START_STATION_ID_COL,END_STATION_ID_COL,BIKE_ID_COL,MODEL_COL)


# Fulfills AC 5: Core logic contained in a dedicated function.
def prepare_data(data_source: str) -> pd.DataFrame:
    """
    Loads the bike-share data and performs essential cleaning (US-1).
    """
    try:
        # Fulfills Functional AC 1: Load the file.
        df = pd.read_csv(data_source)
    except FileNotFoundError:
        # Error handling for robustness
        raise FileNotFoundError(f"Data file not found at: {data_source}")

    # --- GREEN: Make TDD Test Case 2 Pass (Datetime Conversion) ---
    # Fulfills AC 2: Converts string columns to datetime objects.
    df[ START_TIME_COL] = pd.to_datetime(df[START_TIME_COL])
    df[END_TIME_COL] = pd.to_datetime(df[END_TIME_COL])

    # --- GREEN: Make TDD Test Case 1 Pass (Cleaning) ---
    # Define columns that must be present (ensures data integrity).
    critical_columns: List[str] = [TRIP_ID_COL,TRIP_DURATION_COL,START_TIME_COL, END_TIME_COL,USER_TYPE_COL,START_STATION_COL,
                                   END_STATION_COL,START_STATION_ID_COL,END_STATION_ID_COL,BIKE_ID_COL,MODEL_COL]
    # Fulfills AC 3: Drop rows where critical fields are null.
    df.dropna(subset=critical_columns, inplace=True)

    # Fulfills AC 3: Filter out short/invalid trips (e.g., less than 0 seconds).
    df = df[df[TRIP_DURATION_COL] >= 0].copy()

    # The code now runs successfully and returns the cleaned DataFrame.
    return df
