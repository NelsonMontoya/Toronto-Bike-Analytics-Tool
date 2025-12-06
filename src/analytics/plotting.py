# src/analytics/plotting.py

import pandas as pd
import altair as alt



# ================== STANDARDIZED ALTAIR STYLES ==================

BASE_STYLE = {
    "view": {"stroke": "transparent"},
    "background": "white",
}

ALT_AXIS_STYLE = {
    "labelFontSize": 12,
    "titleFontSize": 14,
    "gridOpacity": 0.25,
}

ALT_TITLE_STYLE = {
    "fontSize": 20,
    "anchor": "start",  # left-aligned title
}



# ================== TOP STATIONS PLOT FUNCTION ==================

def plot_top_stations(
    top_df: pd.DataFrame,
    title: str = "Top 10 Busiest Starting Stations",
) -> alt.Chart:
    """
    Create a bar chart for the top starting stations using Altair.

    Parameters
    ----------
    top_df : pd.DataFrame
        DataFrame that must contain a station name column and 'trip_count'.
        Station column can be either 'start_station_name' or 'Start Station Name'.
    title : str, optional
        Title for the chart.

    Returns
    -------
    alt.Chart
        The created Altair Chart object.
    """

    # Try to detect the correct station column
    if "start_station_name" in top_df.columns:
        station_col = "start_station_name"
    elif "Start Station Name" in top_df.columns:
        station_col = "Start Station Name"
    else:
        raise ValueError(
            f"top_df must contain a station column named 'start_station_name' or 'Start Station Name'. "
            f"Found columns: {list(top_df.columns)}"
        )

    if "trip_count" not in top_df.columns:
        raise ValueError(
            f"top_df must contain 'trip_count' column. Found columns: {list(top_df.columns)}"
        )

    chart = (
        alt.Chart(top_df)
        .mark_bar()
        .encode(
            x=alt.X(f"{station_col}:N", title="Start Station Name"),
            y=alt.Y("trip_count:Q", title="Trip Count"),
            tooltip=[station_col, "trip_count"],
        )
        .properties(title=title)
    )

    # Apply standardized Altair styles defined above
    chart = (
        chart.configure(**BASE_STYLE)
        .configure_axis(**ALT_AXIS_STYLE)
        .configure_title(**ALT_TITLE_STYLE)
    )

    return chart
    

def plot_daily_rides(df_daily: pd.DataFrame, title: str = "Daily Ridership Over Time") -> alt.Chart:
    """
    Create a line chart showing total rides per day using Altair.
    """
    df_daily = df_daily.reset_index().rename(columns={df_daily.index.name or "index": "date"})

    chart = (
        alt.Chart(df_daily)
        .mark_line(point=True)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("total_rides:Q", title="Total Rides"),
            tooltip=["date", "total_rides"]
        )
        .properties(title=title)
        .configure(**BASE_STYLE)
        .configure_axis(**ALT_AXIS_STYLE)
        .configure_title(**ALT_TITLE_STYLE)
    )

    return chart



# ================== MANUAL RUNNER ==================
# Allows you to run this file directly:
#    python -m src.analytics.plotting

if __name__ == "__main__":
    print("Running demo plot from plotting.py...")

    # Sample test data
    data = {
        "start_station_name": ["Station A", "Station B", "Station C"],
        "trip_count": [120, 95, 60],
    }

    df_test = pd.DataFrame(data)

    # Call the merged function
    chart = plot_top_stations(df_test, title="Demo: Top Starting Stations")

    # Display the chart
    chart.show()

    print("Chart displayed successfully.")
