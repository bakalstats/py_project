from src.scraping_utils import *


if __name__ == '__main__':
    books_db = pd.DataFrame()
    category_books_urls = get_category_books_urls(input_url=URL_START, book_categories=BOOK_CATEGORIES)
    books_db = get_books_data(category_books_urls)
    books_db.to_parquet(SCRAPED_DATA_FILE)