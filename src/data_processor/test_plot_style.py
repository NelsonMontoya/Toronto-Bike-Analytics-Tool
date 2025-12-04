import pandas as pd
import matplotlib.pyplot as plt

# Import your plot function
from src.analytics.plots import plot_top_starting_stations

# Create some sample data
data = {
    "Start Station Name": ["A", "B", "C", "D", "E"],
    "trip_count": [120, 90, 60, 150, 110]
}

df = pd.DataFrame(data)

# Create the plot (this will automatically apply your style)
fig = plot_top_starting_stations(df)

# Display the plot
plt.show()
