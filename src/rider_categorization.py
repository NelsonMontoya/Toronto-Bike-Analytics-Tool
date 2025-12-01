# src/rider_categorization.py

from typing import Optional
import pandas as pd


def _map_user_type_to_rider_type(raw_value: Optional[object]) -> str:
    """
    Map raw 'User Type' values from the dataset to normalized rider_type categories.

    Rules:
    - Any value containing 'annual'  -> 'Annual member'
    - Any value containing 'casual'  -> 'Casual'
    - Missing, NaN, or anything else -> 'Unknown'
    """
    if pd.isna(raw_value):
        return "Unknown"

    text = str(raw_value).strip().lower()

    if "annual" in text:
        return "Annual member"
    if "casual" in text:
        return "Casual"

    return "Unknown"


def categorize_riders(
    df: pd.DataFrame,
    user_type_col: str = "User Type",
    new_col: str = "rider_type"
) -> pd.DataFrame:
    """
    Add or update a column 'rider_type' based on the 'User Type' column.
    """
    if user_type_col not in df.columns:
        raise KeyError(f"Column '{user_type_col}' not found in DataFrame.")

    df_copy = df.copy()
    df_copy[new_col] = df_copy[user_type_col].apply(_map_user_type_to_rider_type)
    return df_copy


def filter_by_rider_type(
    df: pd.DataFrame,
    rider_type: str,
    rider_type_col: str = "rider_type"
) -> pd.DataFrame:
    """
    Filter rows by standardized rider_type.

    Valid inputs (case-insensitive):
    - 'Annual member', 'annual'
    - 'Casual', 'casual'

    Invalid inputs raise ValueError.
    """
    if rider_type_col not in df.columns:
        raise KeyError(
            f"Column '{rider_type_col}' not found. "
            "Did you call categorize_riders() first?"
        )

    if rider_type is None:
        raise ValueError("rider_type cannot be None.")

    normalized = rider_type.strip().lower()

    if normalized in ("annual member", "annual"):
        target_value = "Annual member"
    elif normalized in ("casual member", "casual"):
        target_value = "Casual"
    else:
        raise ValueError(
            f"Invalid rider_type: {rider_type}. Expected 'Annual member' or 'Casual'."
        )

    return df[df[rider_type_col] == target_value].copy()
