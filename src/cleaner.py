import pandas as pd

def inspect_data(df):
    print("\n=== DATA INSPECTION ===")
    print("\nGeneral info:")
    print(df.info())
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nMissing values per column:")
    print(df.isnull().sum())
    print("\nDuplicate rows count:")
    print(df.duplicated().sum())
    print("\nSample 'nutriments' data:")
    print(df['nutriments'].head(10))

def clean_data(df):
    df_cleaned = df.copy()
    df_cleaned = df_cleaned.dropna(subset=['product_name', 'brands'])
    df_cleaned['categories'] = df_cleaned['categories'].fillna('Unknown')
    df_cleaned['countries'] = df_cleaned['countries'].fillna('Unknown')
    df_cleaned['ingredients_text'] = df_cleaned['ingredients_text'].fillna('Not provided')
    df_cleaned['nutriments'] = df_cleaned['nutriments'].fillna('{}')
    df_cleaned = df_cleaned.drop_duplicates()
    print("\n✓ Data cleaning completed")
    print("  Remaining rows:", len(df_cleaned))
    print("  Missing values after cleaning:", df_cleaned.isnull().sum().to_dict())
    print("  Duplicate rows after cleaning:", df_cleaned.duplicated().sum())
    return df_cleaned