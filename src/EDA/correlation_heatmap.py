import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("../../data/cleaned/openfoodfacts_cleaned.csv")

# Expand the nutriments dictionary
nutriments_expanded = df["nutriments"].apply(lambda x: eval(x) if isinstance(x,str) else x)
nutr_df = pd.json_normalize(nutriments_expanded)

# Select main nutrients (per 100g)
cols = [
    'energy-kcal_100g','fat_100g','saturated-fat_100g','carbohydrates_100g',
    'sugars_100g','fiber_100g','proteins_100g','salt_100g','sodium_100g'
]

nut_df_main = nutr_df[cols]

# Correlation matrix
corr = nut_df_main.corr()

# Heatmap (Matplotlib only)
plt.figure(figsize=(10,8))
plt.imshow(corr, aspect='auto')
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.colorbar()
plt.title("Correlation Heatmap – Main Nutrients (per 100g)")
plt.tight_layout()
plt.show()