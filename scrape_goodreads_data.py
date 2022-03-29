from src.scraping_utils import *


if __name__ == '__main__':
    books_db = pd.DataFrame()
    category_books_urls = get_category_books_urls(input_url=URL_START, book_categories=BOOK_CATEGORIES)
    #  This is close to what was expected, but I think theres three steps that can be explicitly mentioned here
    # 1 Get category urls
    # 2 Retrieve book urls
    # 3 Retrieve book data from urls <--- This is important enough to be seen at top level
    # 4 Save data
    # All of these steps deserve to be visible
    books_db = get_books_data(category_books_urls)
    books_db.to_parquet(SCRAPED_DATA_FILE)