import ast
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned data
df = pd.read_csv("../../data/cleaned/openfoodfacts_cleaned.csv")

#parsing & boxplot
def parse_nutriments(df):
    print("Parsing Nutriments")
    df['nutriments_dict'] = df['nutriments'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) and x != '{}' else {})

    #extract key nutrtional values
    nutritional_fields = {
        'sugars_100g' : 'sugar',
        'fat_100g' : 'fat',
        'energy-kcal_100g' : 'calories',
        'proteins_100g' : 'protein',
        'carbohydrates_100g' : 'carbs',
        'salt_100g' : 'salt',
        'saturated-fat_100g' : 'saturated-fat',
        'fiber_100g' : 'fiber',
        'sodium_100g' : 'sodium'
    }

    for api_key, col_name in nutritional_fields.items():
        df[col_name] = df['nutriments_dict'].apply(lambda x:x.get(api_key, None))

    print(f"Parsed nutriments for {len(df)} products")
    #show statistics
    print("Nutritional data availability:")
    for col_name in nutritional_fields.values():
        non_null = df[col_name].notna().sum()
        print(f"{col_name}:{non_null} ({non_null/len(df)*100:.1f}%")
    return df

#creating boxplot
def boxplots(df, output_dir='visualization'):
    print("Box Plot")
    os.makedirs(output_dir,exist_ok=True)
    #list of nutritional columns to plot
    nutrition_cols = ['sugar','fat','calories','protein','carbs','salt','saturated-fat','fiber','sodium']
    #filter only columns that exist and have data
    available_cols = [col for col in nutrition_cols if col in df.columns and df[col].notna().sum()>0]
    if not available_cols:
        print("No nutritional data available")
        return
    #set style
    sns.set_style("whitegrid")
    #create individual box plot
    for col in available_cols:
        plt.figure(figsize=(10,6))
        #remove outliers for better
        data = df[col].dropna()

        if len(data)==0:
            print(f"Skip {col} , No data")
            continue
        sns.boxplot(x=data,color='skyblue')
        plt.title(f'Distribution of {col.replace("_"," ").title()} (per 100g)', fontsize = 14, fontweight='bold')
        plt.xlabel(f'{col.replace("_"," ").title()}',fontsize =12)
        #statistics
        median=data.median()
        mean= data.mean()
        std= data.std()

        print(f"{col.replace('_', ' ').title():15} | Mean: {mean:6.2f} | Median: {median:6.2f} | Count: {len(data):6} | Std: {std:6.2f}")

        stats_text = f"Mean: {mean:.2f}g\nMedian: {median:.2f}g\nStd: {std:.2f}g"

        plt.text(0.02, 0.98, stats_text,
                 fontsize=11,
                 fontweight='bold',
                 verticalalignment='top',
                 horizontalalignment='left',
                 bbox=dict(facecolor="lightyellow", edgecolor="black", alpha=0.9))

        plt.title(f'Distribution of {col.replace("_", " ").title()} (per 100g)',
                  fontsize=14, fontweight='bold', pad=20)
        plt.xlabel(f'{col.replace("_", " ").title()} (per 100g)', fontsize=12)

        filepath = os.path.join(output_dir,f'boxplot_{col}.png')
        plt.tight_layout()
        plt.savefig(filepath,dpi=300, bbox_inches='tight')
        # plt.show()
        plt.close()
        print(f"saved: {filepath}")
    #create combined plot with all nutrients
    n_cols = len(available_cols)
    n_rows = (n_cols+2) //3 #3 plots per row
    fig, axes = plt.subplots(n_rows,3,figsize=(18,6*n_rows))
    axes = axes.flatten() if n_rows>1 else [axes] if n_cols==1 else axes

    for idx,col in enumerate(available_cols):
        data = df[col].dropna()
        sns.boxplot(x=data,ax=axes[idx], color='lightcoral')
        axes[idx].set_title(f'{col.replace("_"," ").title()}',fontweight='bold')
        axes[idx].set_xlabel('Value per 100g')
    #hide unused subplots
    for idx in range(len(available_cols),len(axes)):
        axes[idx].axis('off')
    combined_filepath = os.path.join(output_dir,'boxplots_all_nutrients.png')
    plt.tight_layout()
    plt.savefig(combined_filepath,dpi=300,bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"Combined plot saved:{combined_filepath}")
    print(f"All box plots created successfully in '{output_dir}/' directory")

def showStatistics(df):
    print("Nutritional Statistics")
    nutrition_cols = ['sugar','fat','calories','protein','carbs','salt','saturated_fat','fiber','sodium']
    available_cols = [col for col in nutrition_cols if col in df.columns]
    stats_df = df[available_cols].describe()
    print(stats_df.round(2))
    return stats_df

df = parse_nutriments(df)
boxplots(df)
showStatistics(df)

parsed_dir = '../data/parsed'
os.makedirs(parsed_dir, exist_ok=True)
df.to_csv(os.path.join(parsed_dir, 'openfoodfacts_parsed.csv'),
         index=False, encoding='utf-8-sig')
print("✓ Parsed data saved!")
