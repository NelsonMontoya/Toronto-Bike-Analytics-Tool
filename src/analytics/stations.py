import pandas as pd

def get_top_starting_stations(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Return top N busiest starting stations.
    """
    df = df.copy()

    # Handle missing names
    df["Start Station Name"] = df["Start Station Name"].fillna("Unknown")

    # Group + count
    station_counts = (
        df.groupby("Start Station Name")
          .size()
          .reset_index(name="trip_count")
          .sort_values("trip_count", ascending=False)
          .head(top_n)
    )

    return station_counts
