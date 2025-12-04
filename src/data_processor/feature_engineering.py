import pandas as pd
from datetime import time, timedelta

# Import constants (assuming they are defined in src.config and src.data_processor.feature_engineering)
# Note: You must ensure all these constants are correctly defined and imported in your environment
from src.config import (
    START_TIME_COL, END_TIME_COL, IS_RUSH_HOUR_COL,
    DURATION_MIN_COL, TRIP_DURATION_COL, AM_RUSH_START,AM_RUSH_END,PM_RUSH_START,PM_RUSH_END
)


def label_rush_hour(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a boolean column indicating if a trip started during rush hour.
    Rush hours are 6:00 to 9:59 (AM) and 16:00 to 18:59 (PM).
    """
    if START_TIME_COL not in df.columns:
        raise KeyError(f"DataFrame must contain '{START_TIME_COL}' column.")

    # Extract time component from datetime objects
    trip_time = df[START_TIME_COL].dt.time

    # AM Rush Hour:
    is_am_rush = (trip_time >= AM_RUSH_START) & (trip_time < AM_RUSH_END)

    # PM Rush Hour:
    is_pm_rush = (trip_time >= PM_RUSH_START) & (trip_time < PM_RUSH_END)

    df[IS_RUSH_HOUR_COL] = is_am_rush | is_pm_rush
    return df


def calculate_trip_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates trip duration in minutes and adds a placeholder for distance (km).
    """
    # Check for required columns
    required_cols = [START_TIME_COL, END_TIME_COL]
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column.")

    # 1. Calculate time difference (timedelta)
    # Temporary column to hold the timedelta object
    df['duration_delta'] = df[END_TIME_COL] - df[START_TIME_COL]

    # 2. Convert timedelta to total seconds and assign to the intermediate column
    # The tests indicate TRIP_DURATION_COL is the column name for duration in seconds
    df[TRIP_DURATION_COL] = df['duration_delta'].dt.total_seconds()

    # 3. Calculate trip duration in minutes
    # This is the line that was failing before, as TRIP_DURATION_COL did not exist.
    df[DURATION_MIN_COL] = df[TRIP_DURATION_COL] / 60.0

    # 4. Add placeholder for distance_km
    df['distance_km'] = 0.0

    # 5. Drop temporary columns
    df.drop(columns=['duration_delta', TRIP_DURATION_COL], inplace=True)

    return df