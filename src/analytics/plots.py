# src/analytics/plots.py

from typing import Optional
import pandas as pd
import altair as alt

from src.analytics.plot_styles import BASE_STYLE, ALT_AXIS_STYLE, ALT_TITLE_STYLE


def plot_top_stations(
    top_df: pd.DataFrame,
    title: str = "Top 10 Busiest Starting Stations",
) -> alt.Chart:
    """
    Create a bar chart for the top starting stations using Altair.

    Parameters
    ----------
    top_df : pd.DataFrame
        DataFrame that must contain 'start_station_name' and 'trip_count' columns.
    title : str, optional
        Title for the chart.

    Returns
    -------
    alt.Chart
        The created Altair Chart object.
    """

    required_cols = {"start_station_name", "trip_count"}
    if not required_cols.issubset(top_df.columns):
        raise ValueError(
            "top_df must contain 'start_station_name' and 'trip_count' columns."
        )

    chart = (
        alt.Chart(top_df)
        .mark_bar()
        .encode(
            x=alt.X("start_station_name:N", title="Start Station Name"),
            y=alt.Y("trip_count:Q", title="Trip Count"),
            tooltip=["start_station_name", "trip_count"],
        )
        .properties(title=title)
    )

    # Apply standardized Altair styles from plot_styles.py
    chart = (
        chart.configure(**BASE_STYLE)
        .configure_axis(**ALT_AXIS_STYLE)
        .configure_title(**ALT_TITLE_STYLE)
    )

    return chart


if __name__ == "__main__":
    # Simple manual test so you can run:
    #   python -m src.analytics.plots
    data = {
        "start_station_name": ["A", "B", "C"],
        "trip_count": [120, 90, 60],
    }
    df = pd.DataFrame(data)
    c = plot_top_stations(df, title="Demo: Top Stations")
    c.show()
