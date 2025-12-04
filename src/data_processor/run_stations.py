# src/run_stations.py

from .data_loader import load_and_clean_data
from .analytics.stations import get_top_starting_stations


def main():
    df = load_and_clean_data()
    print("Loaded rows:", len(df))

    top_stations = get_top_starting_stations(df, top_n=10)
    print("\nTop 10 busiest starting stations:")
    print(top_stations)


if __name__ == "__main__":
    main()
