import matplotlib.pyplot as plt
import seaborn as sns


def apply_standard_plot_style():
    """
    Apply a consistent plotting style across the entire project.
    Call this function at the top of every plotting function.
    """

    # Base theme
    plt.style.use("seaborn-v0_8-whitegrid")

    # Global figure and font settings
    plt.rcParams.update({
        "figure.figsize": (10, 6),        # Standard figure size
        "axes.titlesize": 16,             # Title font size
        "axes.labelsize": 13,             # Axis labels
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "axes.facecolor": "white",
        "figure.facecolor": "white",
        "grid.alpha": 0.3,                # Light grid
    })

    # Consistent color palette for all charts
    sns.set_palette([
        "#2E86C1",  # Blue
        "#28B463",  # Green
        "#CA6F1E",  # Orange
        "#AF7AC5",  # Purple
        "#5DADE2",  # Light Blue
    ])
