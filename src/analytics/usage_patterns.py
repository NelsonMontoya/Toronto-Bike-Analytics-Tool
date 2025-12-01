import pandas as pd


def calculate_daily_rides(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates total rides per day using the start_time column.
    Returns a DataFrame indexed by datetime64[ns] date with column 'total_rides'.
    """

    # Dependency check
    if "start_time" not in df.columns:
        raise KeyError("start_time column is required in the DataFrame.")

    df = df.copy()
    df["start_time"] = pd.to_datetime(df["start_time"])

    # Set datetime index for resampling
    df = df.set_index("start_time")

    # Count rides per day using resample
    daily_counts = df.resample("D").size()

    # Return DataFrame with the required structure
    result = daily_counts.to_frame(name="total_rides")
    result.index.name = "start_time"  # AC 7: index consistency

    return result
