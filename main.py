# main.py

from src.data_loader import load_and_clean_data
from src.rider_categorization import categorize_riders, filter_by_rider_type


def main():
    # 1. Load the dataset
    clean_df = load_and_clean_data()

    # 2. Categorize riders (Annual member / Casual / Unknown)
    df_with_rider_type = categorize_riders(clean_df)

    # 3. Create subsets using the CORRECT rider_type values
    annual_df = filter_by_rider_type(df_with_rider_type, "Annual member")
    casual_df = filter_by_rider_type(df_with_rider_type, "Casual")

    # 4. Optional: see what categories you have
    print("Unique rider_type values:", df_with_rider_type["rider_type"].unique())

    # 5. Debugging output
    print("Total rows:", len(df_with_rider_type))
    print("Annual members:", len(annual_df))
    print("Casual riders:", len(casual_df))


if __name__ == "__main__":
    main()

