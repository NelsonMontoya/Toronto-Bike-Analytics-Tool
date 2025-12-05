import pandas as pd
import pytest
from src.analytics.stations import get_top_starting_stations 
from src.config import START_STATION_COL

# --- Fixture for common test data ---

@pytest.fixture
def sample_data():
    """Provides a sample DataFrame for testing."""
    data = {
        START_STATION_COL: [
            "Station A",
            "Station B",
            "Station A",
            "Station C",
            "Station A",
            "Station B",
            "Station D",
            "Station C",
            "Station E",
            "Station A",
            None, # Missing value test
            "Station B",
            "Station C",
            "Station A",
        ],
        "Some Other Column": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    }
    return pd.DataFrame(data)

# --- Test Cases ---

def test_default_top_n_standard_case(sample_data):
    """Test with default top_n (10) and verifies the counts and order."""
    # Data has 5 trips from Station A, 3 from Station B, 3 from Station C, 1 from Station D, 1 from Station E, 1 from Unknown
    result_df = get_top_starting_stations(sample_data)

    # Check for correct columns and number of rows (top_n=10, but only 6 unique non-empty stations + 1 Unknown)
    assert list(result_df.columns) == [START_STATION_COL, "trip_count"]
    assert len(result_df) == 6 # A, B, C, D, E, Unknown (since top_n > 6, it returns all)

    # Check the top station and count
    assert result_df.iloc[0][START_STATION_COL] == "Station A"
    assert result_df.iloc[0]["trip_count"] == 5

    # Check the second station and count (B and C are tied at 3, so order depends on pandas sort stability)
    # The important part is that the top stations and counts are correct somewhere in the result
    assert {"Station B", "Station C"}.issubset(result_df[START_STATION_COL].values)
    assert all(result_df[result_df[START_STATION_COL].isin(["Station B", "Station C"])]["trip_count"] == 3)


def test_missing_values_are_handled(sample_data):
    """Test that None/NaN values in 'Start Station Name' are correctly replaced with 'Unknown'."""
    result_df = get_top_starting_stations(sample_data, top_n=10)

    # Check if 'Unknown' station exists and has the correct count (1 in the sample data)
    unknown_row = result_df[result_df[START_STATION_COL] == "Unknown"]

    assert not unknown_row.empty
    assert unknown_row.iloc[0]["trip_count"] == 1


def test_custom_top_n(sample_data):
    """Test with a custom value for top_n (e.g., 3)."""
    top_n = 3
    result_df = get_top_starting_stations(sample_data, top_n=top_n)

    # Check for correct number of rows (should be exactly top_n, even with ties)
    # The top 3 should be Station A (5), Station B (3), and Station C (3).
    # Since B and C are tied, the resulting 3 rows could be A, B, C, or A, C, B.
    assert len(result_df) == top_n

    # Check that the counts are correct for the top N.
    expected_counts = {
        "Station A": 5,
        "Station B": 3,
        "Station C": 3,
    }

    # Verify that the top N names and counts match the expected
    actual_names_counts = dict(zip(result_df[START_STATION_COL], result_df["trip_count"]))
    
    assert set(actual_names_counts.keys()).issubset(set(expected_counts.keys()))
    assert all(actual_names_counts.get(k) == v for k, v in expected_counts.items() if k in actual_names_counts)


def test_empty_dataframe():
    """Test function behavior with an empty input DataFrame."""
    empty_df = pd.DataFrame({START_STATION_COL: [], "Some Other Column": []})
    
    result_df = get_top_starting_stations(empty_df)

    # The result should be an empty DataFrame with the correct columns
    assert list(result_df.columns) == [START_STATION_COL, "trip_count"]
    assert result_df.empty