import pandas as pd

df = pd.read_csv("Bike_share data.csv")

# 1. Unique values
print("Unique values in 'User Type':")
print(df["User Type"].dropna().unique())

# 2. Frequency
print("\nValue counts:")
print(df["User Type"].value_counts(dropna=False))
