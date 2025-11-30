import pandas as pd
import pytest
from src.analytics.usage_patterns import calculate_daily_rides


# ----------------------------------------------------------
# Test 1 – AC 5:
# Correct number of rows and total ride counts
# ----------------------------------------------------------
def test_daily_ride_aggregation_counts():
    data = {
        "start_time": [
            *["2024-01-01 08:00:00"] * 10,   # Day 1
            *["2024-01-02 09:00:00"] * 15,   # Day 2
            *["2024-01-03 07:00:00"] * 5,    # Day 3
        ]
    }

    df = pd.DataFrame(data)
    df["start_time"] = pd.to_datetime(df["start_time"])

    result = calculate_daily_rides(df)

    assert len(result) == 3
    assert list(result["total_rides"]) == [10, 15, 5]


# ----------------------------------------------------------
# Test 2 – AC 6:
# Index dtype must be datetime64[ns]
# ----------------------------------------------------------
def test_daily_rides_index_is_datetime64():
    data = {
        "start_time": [
            "2024-01-01 08:00:00",
            "2024-01-01 09:00:00",
            "2024-01-02 10:00:00",
        ]
    }

    df = pd.DataFrame(data)
    df["start_time"] = pd.to_datetime(df["start_time"])

    result = calculate_daily_rides(df)

    assert str(result.index.dtype) == "datetime64[ns]"


# ----------------------------------------------------------
# Test 3 – AC 7:
# Refactor ensures standardized output (column name + index name)
# ----------------------------------------------------------
def test_daily_rides_column_name_and_index_name():
    data = {
        "start_time": [
            "2024-01-01 08:00:00",
            "2024-01-01 09:00:00",
            "2024-01-02 10:00:00",
        ]
    }

    df = pd.DataFrame(data)
    df["start_time"] = pd.to_datetime(df["start_time"])

    result = calculate_daily_rides(df)

    assert "total_rides" in result.columns
    assert result.index.name == "start_time"
