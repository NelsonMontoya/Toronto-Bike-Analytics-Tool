# test/test_rider_categorization.py

import os
import sys

# Ensure project root (Agile_final_project) is on sys.path so 'src' can be imported
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))          # .../Agile_final_project/test
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))   # .../Agile_final_project

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import pytest

from src.data_processor.rider_categorization import (
    categorize_riders,
    filter_by_rider_type,
)


def test_categorize_riders_maps_annual_and_casual_correctly():
    data = {
        "User Type": [
            "Annual Member",
            "Casual Member",
            "annual member",
            "casual",
            "ANNUAL MEMBER",
        ]
    }
    df = pd.DataFrame(data)

    result = categorize_riders(df)

    assert "rider_type" in result.columns

    expected = [
        "Annual member",
        "Casual",
        "Annual member",
        "Casual",
        "Annual member",
    ]
    assert list(result["rider_type"]) == expected


def test_categorize_riders_handles_missing_and_unexpected_values_as_unknown():
    data = {
        "User Type": [
            None,
            float("nan"),
            "VIP",
            "",
        ]
    }
    df = pd.DataFrame(data)

    result = categorize_riders(df)

    assert list(result["rider_type"]) == [
        "Unknown",
        "Unknown",
        "Unknown",
        "Unknown",
    ]


def test_filter_by_rider_type_returns_only_annual_members():
    df = pd.DataFrame({
        "User Type": ["Annual Member", "Casual Member", "Annual Member"],
    })
    df_with_type = categorize_riders(df)

    filtered = filter_by_rider_type(df_with_type, "Annual member")

    assert not filtered.empty
    assert all(filtered["rider_type"] == "Annual member")
    assert len(filtered) == 2


def test_filter_by_rider_type_returns_only_casual_members():
    df = pd.DataFrame({
        "User Type": ["Casual Member", "Annual Member", "Casual Member"],
    })
    df_with_type = categorize_riders(df)

    filtered = filter_by_rider_type(df_with_type, "Casual")

    assert not filtered.empty
    assert all(filtered["rider_type"] == "Casual")
    assert len(filtered) == 2


def test_filter_by_rider_type_raises_error_for_invalid_input():
    df = pd.DataFrame({
        "User Type": ["Casual Member", "Annual Member"],
    })
    df_with_type = categorize_riders(df)

    with pytest.raises(ValueError):
        filter_by_rider_type(df_with_type, "VIP")


def test_filter_by_rider_type_raises_if_rider_type_column_missing():
    df = pd.DataFrame({
        "User Type": ["Casual Member", "Annual Member"],
    })
    with pytest.raises(KeyError):
        filter_by_rider_type(df, "Casual")
        