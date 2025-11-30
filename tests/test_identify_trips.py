import pytest
import pandas as pd
from src.data_processor.identify_trips import (
    label_rush_hour,
    AM_RUSH_START, AM_RUSH_END,
    PM_RUSH_START, PM_RUSH_END
)

# -------------------------------
# Test 1: Boundary AM Start
# -------------------------------
def test_rush_hour_am_boundary_start():
    df = pd.DataFrame({"start_time": ["07:00:00"]})
    df["start_time"] = pd.to_datetime(df["start_time"])
    result = label_rush_hour(df)
    assert result.loc[0, "is_rush_hour"] == True

# -------------------------------
# Test 2: Boundary AM End
# -------------------------------
def test_rush_hour_am_boundary_end():
    df = pd.DataFrame({"start_time": ["09:00:00"]})
    df["start_time"] = pd.to_datetime(df["start_time"])
    result = label_rush_hour(df)
    assert result.loc[0, "is_rush_hour"] is False

# -------------------------------
# Test 3: PM check (16:01)
# -------------------------------
def test_rush_hour_pm_mid():
    df = pd.DataFrame({"start_time": ["16:01:00"]})
    df["start_time"] = pd.to_datetime(df["start_time"])
    result = label_rush_hour(df)
    assert result.loc[0, "is_rush_hour"] is True

# -------------------------------
# Test 4: Missing start_time column
# -------------------------------
def test_missing_start_time_column_raises():
    df = pd.DataFrame({"other_col": [1, 2, 3]})
    with pytest.raises(KeyError):
        label_rush_hour(df)
