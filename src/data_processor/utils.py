# src/data_processor/utils.py
import pandas as pd
from typing import Tuple
from datetime import time
from src.config import START_TIME_COL,DURATION_MIN_COL


def filter_data_advanced(
        df: pd.DataFrame,
        start_time_range: Tuple[time, time],
        min_duration: float,
        max_duration: float
) -> pd.DataFrame:
    """
    Fulfills US-7 AC: Applies advanced filtering criteria to the DataFrame.

    Requires: 'start_time' as datetime object and 'trip_duration_min' as float.
    """

    # ----------------------------------------------------
    # TDD Task 7.2 & 7.4: Implement combined filtering logic (GREEN)
    # ----------------------------------------------------

    # 1. TIME FILTER (Requires converting start_time datetime to a time object)
    start_time_only = df[START_TIME_COL].dt.time
    start_time_min, start_time_max = start_time_range

    time_mask = (start_time_only >= start_time_min) & (start_time_only <= start_time_max)

    # 2. DURATION FILTER
    duration_mask = (df[DURATION_MIN_COL] >= min_duration) & (df[DURATION_MIN_COL] <= max_duration)

    # 3. COMBINED MASK (Applies both criteria simultaneously)
    combined_mask = time_mask & duration_mask

    return df[combined_mask].copy()