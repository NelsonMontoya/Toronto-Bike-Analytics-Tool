import pytest
import pandas as pd
from datetime import datetime
from src.data_processor.feature_engineering import (
    label_rush_hour,
    calculate_trip_metrics,
    AM_RUSH_START, AM_RUSH_END,
    PM_RUSH_START
)

from src.config import START_TIME_COL,IS_RUSH_HOUR_COL,END_TIME_COL,DURATION_MIN_COL,TRIP_ID_COL

# -------------------------------
# Test 1: Boundary AM Start
# -------------------------------
def test_rush_hour_am_boundary_start():
    df = pd.DataFrame({START_TIME_COL: [AM_RUSH_START]})
    df[START_TIME_COL] = pd.to_datetime(df[START_TIME_COL])
    result = label_rush_hour(df)
    assert result.loc[0, IS_RUSH_HOUR_COL] == True

# -------------------------------
# Test 2: Boundary AM End
# -------------------------------
def test_rush_hour_am_boundary_end():
    df = pd.DataFrame({START_TIME_COL: [AM_RUSH_END]})
    df[START_TIME_COL] = pd.to_datetime(df[START_TIME_COL])
    result = label_rush_hour(df)
    assert result.loc[0, IS_RUSH_HOUR_COL] == False

# -------------------------------
# Test 3: PM check (16:01)
# -------------------------------
def test_rush_hour_pm_mid():
    df = pd.DataFrame({START_TIME_COL: [PM_RUSH_START]})
    df[START_TIME_COL] = pd.to_datetime(df[START_TIME_COL])
    result = label_rush_hour(df)
    assert result.loc[0, IS_RUSH_HOUR_COL] == True

# -------------------------------
# Test 4: Missing start_time column
# -------------------------------
def test_missing_start_time_column_raises():
    df = pd.DataFrame({"other_col": [1, 2, 3]})
    with pytest.raises(KeyError):
        label_rush_hour(df)


# =================================================================
# User Story 2: Calculate Trip Duration Metrics
# =================================================================

# Task 2.1: Test for single-day duration (RED -> GREEN).
def test_duration_calculation_singleday():
    """TDD Test 1: Checks duration calculation for a single day trip (15 minutes)."""
    # Arrange: Use the required string format (DD/MM/YYYY HH:MM)
    df_in = pd.DataFrame({
        START_TIME_COL: ['01/01/2025 09:00'],
        END_TIME_COL: ['01/01/2025 09:15']
    })

    # Act
    df_out = calculate_trip_metrics(df_in)

    # Assert 1: Check if the new column exists
    assert DURATION_MIN_COL in df_out.columns
    # Assert 2: Check the calculated value (15 minutes)
    assert df_out[DURATION_MIN_COL].iloc[0] == pytest.approx(15.0)
    # Assert 3: Check that the temporary column was dropped (Refactoring check - Taiga Task 2.5)
    assert 'duration_delta' not in df_out.columns


# Task 2.3: Test for cross-day duration calculation (RED -> GREEN).
def test_duration_calculation_crossday():
    """TDD Test 2: Checks duration calculation for a cross-day trip (20.0 minutes)."""
    # Arrange: Use the required string format (DD/MM/YYYY HH:MM)
    df_in = pd.DataFrame({
        START_TIME_COL: ['02/01/2025 23:50'],
        END_TIME_COL: ['03/01/2025 00:10']
    })

    # Act
    df_out = calculate_trip_metrics(df_in)

    # Assert 1: Check if the new column exists
    assert DURATION_MIN_COL in df_out.columns
    # Assert 2: Check the calculated value (20 minutes)
    assert df_out[DURATION_MIN_COL].iloc[0] == pytest.approx(20.0)
    # Assert 3: Check that the temporary column was dropped (Refactoring check - Taiga Task 2.5)
    assert 'duration_delta' not in df_out.columns


# Task 2.4 (Implied): Test distance column creation
def test_distance_column_created():
    """Checks that the distance_km column is added as a placeholder (AC 1)."""
    df_in = pd.DataFrame({
        START_TIME_COL: ['01/01/2025 09:00'],
        END_TIME_COL: ['01/01/2025 09:15']
    })

    df_out = calculate_trip_metrics(df_in)

    # Assert: The required distance column is created
    assert 'distance_km' in df_out.columns
    # Assert: The placeholder value is 0.0 (as implemented)
    assert df_out['distance_km'].iloc[0] == pytest.approx(0.0)


# Task 2.4 (Implied): Test missing column raises KeyError
def test_missing_time_column_raises():
    """Checks that the function raises KeyError if time columns are missing."""
    df = pd.DataFrame({TRIP_ID_COL: [1]})

    # Check for missing Start Time
    with pytest.raises(KeyError):
        calculate_trip_metrics(df)

    # Check for missing End Time
    df_with_start = pd.DataFrame({START_TIME_COL: ["01/01/2025 09:00"]})
    with pytest.raises(KeyError):
        calculate_trip_metrics(df_with_start)