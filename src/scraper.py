
import requests
import pandas as pd
from datetime import datetime
import os
import time


def get_page_data(page=1, page_size=500, max_retries=3):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?action=process&json=1&page_size={page_size}&page={page}"

    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Warning: Status code {response.status_code} on page {page}. Retry {retries + 1}/{max_retries}")
        except Exception as e:
            print(f"Error fetching page {page}: {e}. Retry {retries + 1}/{max_retries}")
        retries += 1
        time.sleep(2)  # delay between retries

    print(f"✗ Failed to fetch page {page} after {max_retries} retries.")
    return None


def extract_product_info(product):
    return {
        'product_name': product.get('product_name'),
        'brands': product.get('brands'),
        'categories': product.get('categories'),
        'countries': product.get('countries'),
        'ingredients_text': product.get('ingredients_text'),
        'nutriments': str(product.get('nutriments')),  # store as string
        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def scrape_openfoodfacts(num_pages=10, page_size=500, delay=2):
    all_products = []

    print("=" * 60)
    print("OPEN FOOD FACTS API SCRAPER")
    print("=" * 60)
    print(f"Starting to scrape {num_pages} pages...\n")

    for page in range(1, num_pages + 1):
        print(f"Scraping page {page}/{num_pages}...", end=" ")
        data = get_page_data(page=page, page_size=page_size)
        if data and 'products' in data:
            products = data['products']
            if not products:
                print("No more products found. Stopping early.")
                break
            for product in products:
                all_products.append(extract_product_info(product))
            print(f"✓ Found {len(products)} products. Total so far: {len(all_products)}")
        else:
            print("✗ Skipping page due to fetch failure.")

        if page < num_pages:
            time.sleep(delay)

    print("\n" + "=" * 60)
    print(f"Scraping completed! Total products collected: {len(all_products)}")
    print("=" * 60)

    return pd.DataFrame(all_products)


def save_raw_data(df, filename=None):
    raw_data_dir = 'data/raw'
    os.makedirs(raw_data_dir, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"openfoodfacts_raw_{timestamp}.csv"

    filepath = os.path.join(raw_data_dir, filename)
    df.to_csv(filepath, index=False, encoding='utf-8-sig')

    print(f"\n✓ Data saved successfully: {filepath} ({len(df)} rows)")
    return filepath


