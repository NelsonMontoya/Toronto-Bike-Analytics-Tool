import plotly.express as px
import pandas as pd


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
