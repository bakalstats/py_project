import bs4 as bs
import requests
import regex as re
import pandas as pd
from src.config import *


def get_page_body(url: str):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            page = bs.BeautifulSoup(response.text)
            return page.body
    except requests.exceptions.HTTPError as errh:
        print("http error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("connection error:", errc)
    except requests.exceptions.Timeout as errt:
        print("timeout error:", errt)
    except requests.exceptions.RequestException as err:
        print("other error:", err)
    else:
        return None


def clean_text(s: str):
    s = re.sub(r'[\n\t]', ' ', s)
    s = s.strip()
    s = ' '.join(s.split())
    return s


def get_separate_book_urls(url: str):
    page_body = get_page_body(url)
    urls = []
    if page_body:
        urls = [URL_SOURCE + section['href'] for section in page_body.find_all("a", {"class": "bookTitle"})]
    return urls


def get_category_books_urls(
        input_url: str = URL_START,
        book_categories=BOOK_CATEGORIES,
        top_n: int = NUMBER_OF_CATEGORY_PAGES_TO_SCRAPE) -> dict:
    category_urls = {}
    for category in book_categories:
        page_body = get_page_body(input_url + category)
        if not page_body:
            continue
        category_link = page_body.find("div", {"class": "listImgs"}).find("a")["href"]
        top_pages_links = [f"{URL_SOURCE}{category_link}?page={i}" for i in range(1, top_n + 1)]
        category_urls[category] = [book_url for page_url in top_pages_links for book_url in get_separate_book_urls(page_url)]
    return category_urls


def get_text(x):
    return clean_text(getattr(x, "text", ""))


def get_single_book_info(url: str, book_category: str):
    page_body = get_page_body(url)
    book_info = {}
    if page_body:
        book_info["category"] = book_category
        book_info["title"] = get_text(page_body.find("h1", id="bookTitle"))
        book_info["author"] = get_text(page_body.find("span", itemprop="name"))
        book_info["description"] = get_text(page_body.find("div", id="description"))
        book_info["rating"] = get_text(page_body.find("span", itemprop="ratingValue"))
        book_info["number_of_pages"] = get_text(page_body.find("span", itemprop="numberOfPages"))
        book_info["url"] = url
    return book_info


def get_books_data(category_urls: dict):
    books_data = []
    for category in category_urls.keys():
        book_urls = category_urls[category]
        if not book_urls:
            continue
        for book_url in book_urls:
            book_info = get_single_book_info(book_url, category)
            if book_info:
                books_data = books_data.append(book_info)
    return books_data