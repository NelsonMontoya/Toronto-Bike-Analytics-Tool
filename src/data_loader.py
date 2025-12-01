# src/data_loader.py

import pandas as pd

def load_and_clean_data():
    """
    Load and clean the bike share dataset.
    """

    df = pd.read_csv("Bike_share data.csv")   # <-- your file name

    # Clean up column names (optional)
    df.columns = df.columns.str.strip()

    return df
