import ast
from statistics import median

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.core.pylabtools import figsize
from fontTools.misc.cython import returns
from matplotlib.style.core import available
from wordcloud import WordCloud
import os

def main():
    if not os.path.exists("data/cleaned/openfoodfacts_cleaned.csv"):
        print("Error")
        return
    print("Loading")




# Load cleaned data
df = pd.read_csv("data/cleaned/openfoodfacts_cleaned.csv")

# print("\nColumns in dataset:")
# print(df.columns)
# #print(df.head(20))
text = " ".join(str(name) for name in df['product_name'].dropna())
wordcloud = WordCloud(width = 900, height = 900).generate(text)
# Display the generated image:
plt.figure(figsize = (8, 8)) 
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

#bar chart for most country has products

# Count number of products per country

country_counts = df['countries'].value_counts().head(20)  # Top 20 countries

# Create a bar chart

plt.figure(figsize=(12,6))
plt.bar(country_counts.index, country_counts.values, color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.title('Number of Products per Country (Top 20)')
plt.xlabel('Country')
plt.ylabel('Number of Products')
plt.tight_layout()
plt.show()
#its clear that france has the most products 
#bar chart for most product in france 

# Filter data for France

df_france = df[df['countries'].str.contains('France', case=False, na=False)]

# Count top 20 products

top_products = df_france['product_name'].value_counts().head(20)

plt.figure(figsize=(12,6))
plt.bar(top_products.index, top_products.values, color='salmon')
plt.xticks(rotation=90, ha='right')
plt.title('Top 20 Products in France')
plt.xlabel('Product Name')
plt.ylabel('Number of Occurrences')
plt.tight_layout()
plt.show()




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
        plt.axhline(median,color='red',linestyle='--',linewidth=1,label=f'Median: {median:.2f}')
        plt.axhline(mean, color='green', linestyle='--', linewidth=1, label=f'Mean: {mean:.2f}')
        plt.legend()

        filepath = os.path.join(output_dir,f'boxplot_{col}.png')
        plt.tight_layout()
        plt.savefig(filepath,dpi=300, bbox_inches='tight')
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
# في نهاية الملف
df = parse_nutriments(df)
boxplots(df)
showStatistics(df)

# حفظ الداتا
parsed_dir = 'data/parsed'
os.makedirs(parsed_dir, exist_ok=True)
df.to_csv(os.path.join(parsed_dir, 'openfoodfacts_parsed.csv'),
         index=False, encoding='utf-8-sig')
print("✓ Parsed data saved!")