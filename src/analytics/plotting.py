import plotly.express as px
import pandas as pd
from plotly.graph_objects import Figure


def plot_daily_rides(df_daily: pd.DataFrame):
    """
    Produces a Plotly line chart showing total rides per day.
    """

    fig = px.line(
        df_daily,
        x=df_daily.index,
        y="total_rides",
        title="Daily Ridership Over Time",
        labels={
            "x": "Date",
            "total_rides": "Total Rides"
        }
    )

    return fig


def plot_duration_histogram(df: pd.DataFrame) -> Figure:  # <- updated type hint
    """
    Generates a Plotly histogram of trip duration, comparing Subscribers and Casual riders.
    Fulfills US-8.
    """
    # Defensive check for required columns
    if 'trip_duration_min' not in df.columns or 'User Type' not in df.columns:
        raise KeyError("DataFrame must contain 'trip_duration_min' and 'User Type' columns.")

    # Apply data filtering (Refactor step for better visualization, clipping long trips)
    MAX_DURATION = 60
    df_filtered = df[df['trip_duration_min'] <= MAX_DURATION]

    fig = px.histogram(
        df_filtered,
        x='trip_duration_min',
        color='User Type',
        barmode='overlay',  # Overlays the two distributions
        nbins=30,
        title='Trip Duration Distribution by Rider Type (Capped at 60 min)',
        labels={
            "trip_duration_min": "Trip Duration (Minutes)",
            "count": "Number of Trips"  # Plotly default label for y-axis count
        }
    )

    # Task 8.4 (Refactor): Standardized Plotting (US-12 Compliance)
    # Ensure transparency for overlay clarity and consistent layout
    fig.update_traces(opacity=0.75)
    fig.update_layout(
        xaxis_title="Trip Duration (Minutes)",
        yaxis_title="Number of Trips",
        # Standardized Plotting: Ensure clear layout
        margin=dict(l=20, r=20, t=50, b=20),
        # Ensures the plot does not extend beyond the 60-minute cap
        xaxis=dict(range=[0, MAX_DURATION])
    )

    return fig