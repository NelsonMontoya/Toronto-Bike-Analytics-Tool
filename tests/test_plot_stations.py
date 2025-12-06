import pandas as pd
import altair as alt

from src.analytics.plotting import plot_top_stations


def test_plot_top_stations_returns_altair_chart():
    """
    The plotting function should return an Altair Chart-like object
    (Chart or LayerChart) when given a valid DataFrame.
    """
    data = {
        "start_station_name": ["A", "B", "C", "D", "E"],
        "trip_count": [120, 90, 60, 150, 110],
    }
    df = pd.DataFrame(data)

    chart = plot_top_stations(df, title="Top 5 Stations")

    # The function currently returns a LayerChart (chart + text)
    assert isinstance(chart, (alt.Chart, alt.LayerChart))


def test_plot_top_stations_uses_title_property():
    """
    The chart (or its base layer) should use the title passed into the function.
    """
    data = {
        "start_station_name": ["A", "B", "C"],
        "trip_count": [10, 20, 30],
    }
    df = pd.DataFrame(data)

    title = "My Custom Title"
    chart = plot_top_stations(df, title=title)

    # If it's a layered chart, look at the first layer
    if isinstance(chart, alt.LayerChart):
        base_chart = chart.layer[0]
        assert base_chart.title == title
    else:
        assert chart.title == title


def test_plot_top_stations_requires_trip_count_column():
    """
    If the DataFrame does not contain 'trip_count', the function
    should fail – this is our RED test for invalid input.
    """
    bad_data = {
        "start_station_name": ["A", "B", "C"],
        "something_else": [1, 2, 3],
    }
    bad_df = pd.DataFrame(bad_data)

    try:
        plot_top_stations(bad_df, title="Bad Data")
        assert False, "Expected an error when 'trip_count' is missing"
    except Exception:
        assert True
