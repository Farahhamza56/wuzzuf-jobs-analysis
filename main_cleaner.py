from src.cleaner import inspect_data, clean_data
import pandas as pd
import os


def main():
    print("\nOPEN FOOD FACTS DATA CLEANING\n")

    raw_dir = 'data/raw'

    if not os.path.exists(raw_dir):
        print(f"✗ Error: Directory '{raw_dir}' not found!")
        print("Please run main_scraper.py first to collect data.")
        return

    raw_files = [f for f in os.listdir(raw_dir) if f.endswith('.csv')]

    if not raw_files:
        print(f"✗ Error: No CSV files found in '{raw_dir}'!")
        print("Please run main_scraper.py first to collect data.")
        return

    # Use the most recent file
    raw_files.sort()
    latest_file = raw_files[-1]
    raw_filepath = os.path.join(raw_dir, latest_file)

    print(f"Found raw data file: {latest_file}")
    input("Press Enter to start cleaning...")

    # Load raw data
    print(f"\nLoading raw data from: {raw_filepath}")
    df = pd.read_csv(raw_filepath, encoding='utf-8-sig')
    print(f"✓ Loaded {len(df)} rows\n")


    inspect_data(df)
    df_cleaned = clean_data(df)


    cleaned_dir = 'data/cleaned'
    os.makedirs(cleaned_dir, exist_ok=True)

    cleaned_filepath = os.path.join(cleaned_dir, 'openfoodfacts_cleaned.csv')


    df_cleaned.to_csv(cleaned_filepath, index=False, encoding='utf-8-sig')

    print(f"\n✓ Cleaned data saved: {cleaned_filepath}")


if __name__ == "__main__":
    main()