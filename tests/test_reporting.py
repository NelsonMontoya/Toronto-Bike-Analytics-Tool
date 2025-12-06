import pytest
import pandas as pd
import os
import matplotlib.pyplot as plt

# This import will cause the initial failure (RED)
from src.analytics.plotting import plot_duration_histogram


@pytest.fixture
def mock_analytical_df():
    """
    Mock DataFrame representing the analytical data after US-2/US-3 processing.
    The plot requires 'trip_duration_min' and 'User Type'.
    """
    return pd.DataFrame({
        'trip_duration_min': [10.5, 50.2, 12.0, 8.5, 30.0, 7.1],
        'User Type': ['Subscriber', 'Casual', 'Subscriber', 'Subscriber', 'Casual', 'Casual'],
    })


def test_plot_duration_histogram_returns_object(mock_analytical_df, tmp_path):
    """
    Asserts that the function executes successfully, returns a Plotly Figure,
    and optionally saves the figure to a file.
    """
    output_path = tmp_path / "duration_histogram.png"

    # ACT: Run the plotting function
    fig = plot_duration_histogram(mock_analytical_df)

    # ASSERT 1: Check if a plotly Figure object is returned
    from plotly.graph_objects import Figure
    assert fig is not None
    assert isinstance(fig, Figure)

    # ASSERT 2: Optionally save the figure and check file existence
    fig.write_image(str(output_path))
    assert os.path.exists(output_path)