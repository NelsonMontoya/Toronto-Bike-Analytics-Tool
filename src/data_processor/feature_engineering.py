import pandas as pd
from datetime import time
from typing import List, Dict
from src.config import AM_RUSH_START,AM_RUSH_END,PM_RUSH_START,PM_RUSH_END,START_TIME_COL,END_TIME_COL,TRIP_DURATION_COL


# ============================================================
# Core Logic Function (AC 1)
# ============================================================
def label_rush_hour(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a Boolean column `is_rush_hour` to the DataFrame based on
    the trip start_time.

    Rush hour windows:
    - AM: 07:00:00 to 08:59:59
    - PM: 16:00:00 to 17:59:59

    AC Requirements:
    - Must raise an exception if start_time not present (AC 4)
    - Must add boolean is_rush_hour column (AC 2)
    """

    # ---------------------------
    # AC 4: Dependency Check
    # ---------------------------
    if START_TIME_COL not in df.columns:
        raise KeyError("Input DataFrame must contain a 'Start Time' column.")

    # Ensure datetime type
    if not pd.api.types.is_datetime64_any_dtype(df[START_TIME_COL]):
        df[START_TIME_COL] = pd.to_datetime(df[START_TIME_COL], errors="coerce")

    # Extract time object from datetime
    start_times = df[START_TIME_COL].dt.time

    # ---------------------------
    # AC 3: Rush hour logic
    # Vectorized conditions for performance (AC 1)
    # ---------------------------
    is_am_rush = (start_times >= AM_RUSH_START) & (start_times <= AM_RUSH_END)
    is_pm_rush = (start_times >= PM_RUSH_START) & (start_times <= PM_RUSH_END)

    df["is_rush_hour"] = is_am_rush | is_pm_rush

    return df


# ============================================================
# Core Logic Function (US-2)
# ============================================================
def calculate_trip_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates essential trip metrics: duration in minutes and a distance proxy.
    Fulfills TDD Story US-2.
    """

    # ---------------------------
    # Dependency Check & Resilience (Addressing the format issue)
    # ---------------------------
    if START_TIME_COL not in df.columns or END_TIME_COL not in df.columns:
        raise KeyError(f"Input DataFrame must contain '{START_TIME_COL}' and '{END_TIME_COL}' columns.")

    # Check and convert to datetime if they are still string objects
    # Assuming US-1 is done, but adding safety conversion based on user's format:
    if not pd.api.types.is_datetime64_any_dtype(df[START_TIME_COL]):
        df[START_TIME_COL] = pd.to_datetime(df[START_TIME_COL], format='%d/%m/%Y %H:%M', errors="coerce")
    if not pd.api.types.is_datetime64_any_dtype(df[END_TIME_COL]):
        df[END_TIME_COL] = pd.to_datetime(df[END_TIME_COL], format='%d/%m/%Y %H:%M', errors="coerce")

    # ---------------------------
    # Taiga Task 2.2 & 2.4: Duration calculation
    # ---------------------------

    # 1. Calculate Timedelta
    # df['duration_delta'] = df[END_TIME_COL] - df[START_TIME_COL]

    # 2. Convert Timedelta to total minutes.
    # df['trip_duration_min'] = df['duration_delta'].dt.total_seconds() / 60.0
    df['trip_duration_min'] = df[TRIP_DURATION_COL] / 60.0


    # Functional AC 1 Proxy: Distance Calculation
    # df['distance_km'] = 0.0  # Placeholder for distance

    # Taiga Task 2.5 (Refactor): Drop the temporary column
    # df.drop(columns=['duration_delta'], errors='ignore', inplace=True)

    return df