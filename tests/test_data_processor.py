import pandas as pd
import pytest
# Import the function we are about to test (it will cause the initial failure)
from src.data_processor.loading_cleaning import prepare_data

# Taiga Task 1.1: Write failing test for null row count (RED).
# Taiga Task 1.3: Write failing test for datetime conversion (RED).

@pytest.fixture
def mock_data():
    """
        Creates a mock DataFrame (6 rows) using the user's column names.

        Problematic rows for US-1 cleaning:
        - Row 3 (Index 2): 'Trip Duration' is 0 (Invalid Trip).
        - Row 4 (Index 3): 'Start Time' is None and 'Start Station Id' is None (Critical Nulls).

        Expected remaining rows after cleaning: 6 - 2 = 4.
    """
    return pd.DataFrame({
        # Columns used for cleaning/conversion:
        'Trip Id': [1, 2, 3, 4, 5, 6],
        'Start Time': ['2025-01-01 07:30:00', '2025-01-01 10:00:00', '2025-01-01 16:15:00',
                       None, '2025-01-02 23:50:00', '2025-01-03 09:00:00'],  # <-- Null in Row 4
        'End Time': ['2025-01-01 07:45:30', '2025-01-01 10:20:00', '2025-01-01 16:15:00',
                     '2025-01-01 12:00:00', '2025-01-03 00:10:00', '2025-01-03 09:15:30'],
        'Start Station Id': [100, 101, 102, 200, 104, 105],
        'Trip  Duration': [900, 1200, 0, 500, 1000, 800],

        # Remaining columns (filled with non-null placeholders):
        'End Station Id': [110, 111, 112, 113, 114, 115],
        'Start Station Name': [f'S{i}' for i in range(6)],
        'End Station Name': [f'E{i}' for i in range(6)],
        'Bike Id': [10001, 10002, 10003, 10004, 10005, 10006],
        'User Type': ['Subscriber', 'Casual', 'Subscriber', 'Casual', 'Subscriber', 'Subscriber'],
        'Model': ['A', '', 'A', 'A', 'B', 'B'],
    })


def test_data_drops_critical_nulls(mock_data, tmp_path):
    """Fulfills AC 3 & Test Case 1: Asserts correct number of rows after cleaning."""
    temp_file = tmp_path / "test_data_nulls.csv"
    mock_data.to_csv(temp_file, index=False)

    expected_rows = 4  # 6 initial rows - 2 bad rows = 4
    clean_df = prepare_data(str(temp_file))

    # This assertion initially fails because the cleaning logic in prepare_data is missing.
    assert len(clean_df) == expected_rows


def test_datetime_conversion(mock_data, tmp_path):
    """Fulfills AC 2 & Test Case 2: Asserts that time columns are true datetime objects."""
    temp_file = tmp_path / "test_data_datetime.csv"
    mock_data.to_csv(temp_file, index=False)

    clean_df = prepare_data(str(temp_file))

    # This assertion initially fails because the conversion logic in prepare_data is missing.
    assert pd.api.types.is_datetime64_any_dtype(clean_df['Start Time'])
    assert pd.api.types.is_datetime64_any_dtype(clean_df['End Time'])