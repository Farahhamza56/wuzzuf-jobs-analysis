from src.scraping.scraper import scrape_openfoodfacts, save_raw_data

def main():
    print("\nOPEN FOOD FACTS DATA SCRAPER - FINAL RUN\n")

    NUM_PAGES = 40
    PAGE_SIZE = 100
    DELAY = 2

    print(f"Configuration:")
    print(f"  - Pages to scrape: {NUM_PAGES}")
    print(f"  - Products per page: {PAGE_SIZE}")
    print(f"  - Delay between pages: {DELAY} seconds\n")

    input("Press Enter to start scraping...")

    df = scrape_openfoodfacts(num_pages=NUM_PAGES, page_size=PAGE_SIZE, delay=DELAY)
    filepath = save_raw_data(df)

    print("\n✓ FULL DATA COLLECTION COMPLETED!")
    print(f"  CSV file ready for inspection & cleaning: {filepath}\n")


if __name__ == "__main__":
    main()
