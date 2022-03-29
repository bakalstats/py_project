
GOODREADS_URL = "https://www.goodreads.com/"
GOODREADS_TAG_URL = f"{GOODREADS_URL}list/tag/"
URL_SOURCE = "https://www.goodreads.com/"
URL_START = "https://www.goodreads.com/list/tag/"
SCRAPED_DATA_PATH = "data/goodreads_data.parquet"
OUTPUT_PATH = "data/goodreads_data.parquet"
SCRAPED_DATA_FILE = "data/goodreads_data.parquet"
NUMBER_OF_CATEGORY_PAGES_TO_SCRAPE = 5
BOOK_CATEGORIES = [
    "romance",
    "fiction",
    "young-adult",
    "fantasy",
    "science-fiction",
    "non-fiction",
    "children",
    "history",
    "covers",
    "mystery",
    "horror",
    "best",
    "historical-fiction",
    "gay",
    "paranormal",
    "love",
    "titles",
    "contemporary",
    "middle-grade",
    "historical-romance",
    "biography",
    "thriller",
    "series",
    "women",
    "nonfiction",
    "classics",
    "lgbt",
    "graphic-novels",
    "memoir",
    "queer",
]
CATEGORY_COL = "category"
TITLE_COL = "title"
AUTHOR_COL = "author"
DESCRIPTION_COL = "description"
RATING_COL = "rating"
PAGES_COL = "number_of_pages"
TEXT_COL = "text"
LABEL_COL = "category"
CLASSIFICATION_THRESHOLD = 0.2

