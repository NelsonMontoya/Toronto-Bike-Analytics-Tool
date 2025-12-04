

from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
from src.analytics.plot_styles import apply_standard_plot_style


def plot_top_starting_stations(
    top_df: pd.DataFrame,
    title: str = "Top 10 Busiest Starting Stations",
):
    """
    Create a bar chart for the top starting stations.

    Parameters
    ----------
    top_df : pd.DataFrame
        Output from get_top_starting_stations(); must contain
        'Start Station Name' and 'trip_count' columns.
    title : str, optional
        Title for the chart.

    Returns
    -------
    matplotlib.figure.Figure
        The created Matplotlib Figure object.

    """
    # Apply global style
    apply_standard_plot_style()

    #validate columns
    required_cols = {"Start Station Name", "trip_count"}
    if not required_cols.issubset(top_df.columns):
        raise ValueError("top_df must contain 'Start Station Name' and 'trip_count' columns.")

    # Make a copy so we don't modify the caller's DataFrame
    df_plot = top_df.copy()
    
    # Create numeric positions for x-axis 
    x_positions =list(range(len(df_plot)))

    # Create figure (global style controls)
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Labels
    ax.bar(df_plot["Start Station Name"], df_plot["trip_count"])
    ax.set_xlabel("Start Station Name")
    ax.set_ylabel("Trip Count")
    ax.set_title(title)

    # Rotate x labels for readability
    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(df_plot["Start Station Name"], rotation=45, ha="right")

    fig.tight_layout()
    return fig
