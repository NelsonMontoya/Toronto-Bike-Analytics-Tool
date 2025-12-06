import pandas as pd

from src.config import START_STATION_COL

def get_top_starting_stations(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Return top N busiest starting stations.
    """
    df = df.copy()

    # Handle missing names
    df[START_STATION_COL] = df[START_STATION_COL].fillna("Unknown")

    # Group + count
    station_counts = (
        df.groupby(START_STATION_COL)
          .size()
          .reset_index(name="trip_count")
          .sort_values("trip_count", ascending=False)
          .head(top_n)
    )

    return station_counts