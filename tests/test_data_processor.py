import pandas as pd
import pytest
import datetime

from src.data_processor.utils import filter_data_advanced  # Target function
from src.config import START_TIME_COL,TRIP_DURATION_COL


@pytest.fixture
def mock_advanced_filter_data():
    """
    Creates mock data to test time and duration range filters (US-7).
    Total 5 rows.
    """
    return pd.DataFrame({
        START_TIME_COL: [
            datetime.datetime(2025, 1, 1, 7, 30, 0),  # Row 1: Too early (Time out), Duration 10
            datetime.datetime(2025, 1, 1, 9, 0, 0),  # Row 2: Good time, Duration 15 (GOOD)
            datetime.datetime(2025, 1, 1, 9, 30, 0),  # Row 3: Good time, Duration 25 (Duration out)
            datetime.datetime(2025, 1, 1, 10, 30, 0),  # Row 4: Too late (Time out), Duration 15
            datetime.datetime(2025, 1, 1, 9, 0, 0)  # Row 5: Good time, Duration 5 (Duration out)
        ],
        TRIP_DURATION_COL: [10.0, 15.0, 25.0, 15.0, 5.0]
    })


# Fulfills Taiga Task 7.1: Write failing test for time range filter (RED).
def test_advanced_filter_time(mock_advanced_filter_data):
    """TDD US-7 Test 1: Checks filtering by a time range (08:00 AM to 10:00 AM)."""

    df_out = filter_data_advanced(
        df=mock_advanced_filter_data,
        start_time_range=(datetime.time(8, 0), datetime.time(10, 0)),
        min_duration=0.0,  # Neutral duration filter
        max_duration=100.0  # Neutral duration filter
    )
    # Expected: Rows 2 and 3 should remain (Trips started at 9:00 and 9:30). Expected length = 2.
    assert len(df_out) == 3
    assert all(df_out.index.isin([1, 2,4]))


# Fulfills Taiga Task 7.3: Write failing test for combined filter (RED).
def test_advanced_filter_combined(mock_advanced_filter_data):
    """TDD US-7 Test 3: Checks filtering by both time (8-10 AM) AND duration (10-20 min)."""

    df_out = filter_data_advanced(
        df=mock_advanced_filter_data,
        start_time_range=(datetime.time(8, 0), datetime.time(10, 0)),
        min_duration=10.0,
        max_duration=20.0
    )
    # Expected: Row 2 only.
    # Row 1 (7:30) is out by time. Row 3 (25 min) is out by duration.
    # Row 4 (10:30) is out by time. Row 5 (5 min) is out by duration.
    assert len(df_out) == 1
    assert df_out.index[0] == 1

