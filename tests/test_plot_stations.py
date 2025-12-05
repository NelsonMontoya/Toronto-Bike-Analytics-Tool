import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pytest

from src.analytics import plot_top_stations


def test_plot_top_starting_stations_returns_figure():
    """
    The plotting function should return a Matplotlib Figure
    when given a valid DataFrame.
    """
    data = {
        "Start Station Name": ["A", "B", "C", "D", "E"],
        "trip_count": [120, 90, 60, 150, 110],
    }
    df = pd.DataFrame(data)

    fig = plot_top_stations(df)

    # Check type
    assert isinstance(fig, Figure)

    # Optional: close figure to avoid resource warnings
    plt.close(fig)


def test_plot_top_starting_stations_raises_error_for_missing_columns():
    """
    The plotting function should raise ValueError if the
    required columns are missing.
    """
    # Missing 'trip_count' column
    bad_data = {
        "Start Station Name": ["A", "B", "C"],
        "something_else": [1, 2, 3],
    }
    bad_df = pd.DataFrame(bad_data)

    with pytest.raises(ValueError):
        plot_top_stations(bad_df)


def test_plot_top_starting_stations_uses_default_title():
    """
    The default title should be 'Top 10 Busiest Starting Stations'
    when no custom title is provided.
    """
    data = {
        "Start Station Name": ["A", "B", "C"],
        "trip_count": [10, 20, 30],
    }
    df = pd.DataFrame(data)

    fig = plot_top_stations(df)

    # Get the Axes from the Figure and check the title
    ax = fig.axes[0]
    assert ax.get_title() == "Top 10 Busiest Starting Stations"

    plt.close(fig)
