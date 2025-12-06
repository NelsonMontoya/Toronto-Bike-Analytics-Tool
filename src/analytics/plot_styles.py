# src/analytics/plot_styles.py

import matplotlib.pyplot as plt
import altair as alt

#  Base style for Altair charts
BASE_STYLE = {
    "background": "white",
    "padding": 10,
}

#  Optional: axis + title styles for Altair
ALT_AXIS_STYLE = {
    "labelFont": "Arial",
    "titleFont": "Arial",
    "labelFontSize": 11,
    "titleFontSize": 13,
}

ALT_TITLE_STYLE = {
    "font": "Arial",
    "fontSize": 18,
    "anchor": "start",
}


def apply_standard_plot_style():
    """
    Apply a standard Matplotlib style across all charts.

    This function mainly affects Matplotlib figures.
    Call it at the start of plotting functions that use plt.
    """
    plt.rcParams.update(
        {
            "figure.figsize": (10, 6),
            "axes.titlesize": 16,
            "axes.labelsize": 12,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "axes.grid": True,
            "grid.alpha": 0.3,
        }
    )


if __name__ == "__main__":
    # Quick sanity check when running:
    print("Plot styles loaded successfully.")
    print("BASE_STYLE:", BASE_STYLE)
