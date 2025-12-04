import pandas as pd
import pytest
import datetime


from src.data_processor.utils import filter_data_advanced
from src.config import START_TIME_COL, DURATION_MIN_COL


# --- Fixture for Sample Data ---
@pytest.fixture
def mock_advanced_filter_data():
    """
    Creates mock data to test time, duration, AND date range filters.
    Total 7 rows, covering different exclusion reasons.
    """
    return pd.DataFrame({
        START_TIME_COL: [
            datetime.datetime(2025, 1, 5, 7, 30, 0),  # Row 0: Too early (Time out), Date IN, Duration 10
            datetime.datetime(2025, 1, 10, 9, 0, 0),  # Row 1: Good time, Date IN, Duration 15 (GOOD ROW)
            datetime.datetime(2025, 1, 10, 9, 30, 0),  # Row 2: Good time, Date IN, Duration 25 (Duration out)
            datetime.datetime(2025, 1, 15, 10, 30, 0),  # Row 3: Too late (Time out), Date IN, Duration 15
            datetime.datetime(2025, 1, 10, 9, 0, 0),  # Row 4: Good time, Date IN, Duration 5 (Duration out)
            datetime.datetime(2025, 1, 2, 8, 30, 0),  # Row 5: Date OUT (Too early), Good Time, Duration 15
            datetime.datetime(2025, 1, 20, 9, 0, 0),  # Row 6: Date OUT (Too late), Good Time, Duration 15
        ],
        # FIX: Use DURATION_MIN_COL to match the column name expected by the filter function
        DURATION_MIN_COL: [10.0, 15.0, 25.0, 15.0, 5.0, 15.0, 15.0]
    })


# --- Neutral Filter Constants (for date/time tests) ---
NEUTRAL_START_DATE = datetime.date(2025, 1, 1)
NEUTRAL_END_DATE = datetime.date(2025, 1, 31)
NEUTRAL_MIN_DURATION = 0.0
NEUTRAL_MAX_DURATION = 100.0


# Fulfills Taiga Task 7.1: Checks filtering by time range.
def test_advanced_filter_time(mock_advanced_filter_data):
    """TDD US-7 Test 1: Checks filtering by a time range (08:00 AM to 10:00 AM)."""

    df_out = filter_data_advanced(
        df=mock_advanced_filter_data,
        start_time_range=(datetime.time(8, 0), datetime.time(10, 0)),
        min_duration=NEUTRAL_MIN_DURATION,
        max_duration=NEUTRAL_MAX_DURATION,
        start_date=NEUTRAL_START_DATE,
        end_date=NEUTRAL_END_DATE
    )
    # Expected: Rows 1, 2, 4 (Time IN: 9:00, 9:30, 9:00).
    # Row 0 (7:30) is out by time. Row 3 (10:30) is out by time.
    # Rows 5 & 6 are OUT by NEUTRAL date filter (Jan 1 to Jan 31) because their dates are Jan 2 and Jan 20.
    # Rerunning expected logic (7 rows total):
    # Time OUT: 0 (7:30), 3 (10:30)
    # Duration OUT: None
    # Date IN (Jan 1 to Jan 31): All 7 rows are IN.
    # Therefore, expected rows IN: 5 (0, 1, 2, 4, 6)
    # Corrected expected length based on Time Out (0, 3) logic and assuming date filter includes all:
    # Expected length = 5 (Rows 1, 2, 4, 5, 6)
    assert len(df_out) == 5
    assert all(df_out.index.isin([1, 2, 4, 5, 6]))


# Fulfills Taiga Task 7.3: Checks filtering by combined time/duration.
def test_advanced_filter_combined(mock_advanced_filter_data):
    """TDD US-7 Test 3: Checks filtering by both time (8-10 AM) AND duration (10-20 min), with neutral date."""

    df_out = filter_data_advanced(
        df=mock_advanced_filter_data,
        start_time_range=(datetime.time(8, 0), datetime.time(10, 0)),
        min_duration=10.0,
        max_duration=20.0,
        start_date=NEUTRAL_START_DATE,
        end_date=NEUTRAL_END_DATE
    )
    # Row 0 (7:30) is out by time.
    # Row 1 (Time IN, Duration 15) is IN.
    # Row 2 (Time IN, Duration 25) is out by duration.
    # Row 3 (10:30) is out by time.
    # Row 4 (Time IN, Duration 5) is out by duration.
    # Row 5 (Time 8:30, Duration 15) is IN.
    # Row 6 (Time 9:00, Duration 15) is IN.
    # Expected: Rows 1, 5, 6. Expected length = 3
    assert len(df_out) == 3
    assert all(df_out.index.isin([1, 5, 6]))


# Fulfills TDD requirement for new date filtering
def test_advanced_filter_date(mock_advanced_filter_data):
    """
    TDD US-X Test 4: Checks filtering specifically by date range.
    Filters from Jan 5th to Jan 15th, excluding dates outside this window.
    """

    # Define tight date filter: Jan 5th, 2025, to Jan 15th, 2025
    test_start_date = datetime.date(2025, 1, 5)
    test_end_date = datetime.date(2025, 1, 15)

    # Use neutral time/duration filters
    test_start_time = datetime.time(0, 0)
    test_end_time = datetime.time(23, 59)

    df_out = filter_data_advanced(
        df=mock_advanced_filter_data,
        start_time_range=(test_start_time, test_end_time),
        min_duration=NEUTRAL_MIN_DURATION,
        max_duration=NEUTRAL_MAX_DURATION,
        start_date=test_start_date,
        end_date=test_end_date
    )

    # Rows with dates outside 01/05-01/15:
    # Row 5 (Date: Jan 2nd) -> OUT
    # Row 6 (Date: Jan 20th) -> OUT
    # Rows to keep: 0, 1, 2, 3, 4 (All have dates within range)
    # Expected: 7 total rows - 2 excluded = 5 rows
    assert len(df_out) == 5
    assert all(df_out.index.isin([0, 1, 2, 3, 4]))