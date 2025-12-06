import pandas as pd
import altair as alt

def plot_top_stations(top_stations_df: pd.DataFrame, title: str) -> alt.Chart:
    """
    Plots the top starting stations as a horizontal bar chart and returns the Altair chart object.
    
    Args:
        top_stations_df: DataFrame containing the station column and 'trip_count'.
        title: The title for the chart.
    
    Returns:
        An Altair Chart object (the figure).
    """
    
    # Assuming the station column name is consistent with the earlier context
    station_col_name = top_stations_df.columns[0] 
    
    # 1. Create the base bar chart
    chart = alt.Chart(top_stations_df).mark_bar().encode(
        # Y-axis: Station Name. Sort by '-x' (trip_count) descending.
        x=alt.X(station_col_name, title="Start Station", sort="-x"),
        # X-axis: Trip Count.
        y=alt.Y("trip_count", title="Trip Count"),
        tooltip=[station_col_name, "trip_count"]
    ).properties(
        title=title
    ).interactive()

    # 2. Add text labels
    text = chart.mark_text(
        align="left",
        baseline="middle",
        dx=3 
    ).encode(
        text=alt.Text("trip_count", format=","),
        color=alt.value("black")
    )

    # 3. Combine and RETURN the final figure (chart object)
    return chart + text