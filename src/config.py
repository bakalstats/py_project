URL_SOURCE = "https://www.goodreads.com/"
URL_START = f"{URL_SOURCE}list/tag/"
SCRAPED_DATA_FILE = "data/goodreads_data.parquet"
DATA_EMBEDDINGS_FILE = "data/goodreads_data_embeddings.parquet"
PRETRAINED_SEMANTIC_SEARCH_MODEL = "msmarco-distilbert-base-dot-prod-v3"
LOCAL_SEARCH_MODEL_PATH = "data/search_model/"
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
EMBEDDINGS_COL = "embeddings"
DISTANCE_COL = "distance"
CLASSIFICATION_THRESHOLD = 0.2
TEST_SET_SHARE = 0.2
