import requests
import bs4 as bs
def get_page_body(url: str):
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.HTTPError as errh:
        print ("http error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("conection error:",errc)
    except requests.exceptions.Timeout as errt:
        print ("timeout error:",errt)
    except requests.exceptions.RequestException as err:
        print ("other error:",err)
        
    if response.status_code == 200:
        page = bs.BeautifulSoup(response.text)
        return page.body
    else:
        return None
    
def clean_text(s: str):
    s = re.sub(r'[\n\t]', ' ', s)
    s = s.strip()
    s = ' '.join(s.split())
    return s

    
def get_category_urls(input_url: str = URL_START, top_n:int = 1) -> dict:
    category_urls = {}
    for category in BOOK_CATEGORIES:
        page_body = get_page_body(input_url + category)
        if page_body:
            link = page_body.find("div",{"class": "listImgs"}).find("a")['href']
            links = ["https://www.goodreads.com/" + link + f"?page={i}" for i in range(1,top_n+1)]
            category_urls[category] = links
    return category_urls


def get_separate_book_urls(url: str):
    page_body = get_page_body(url)
    urls = []
    if page_body:
        for section in page_body.find_all("a",{"class": "bookTitle"}):
            link = URL_SOURCE + section['href']
            urls.append(link)
    return urls


def get_text(x):
    return clean_text(getattr(x, "text", ""))


def get_book_info(url: str, book_category: str):
    page_body = get_page_body(url)
    book_info = {}
    if page_body:
        book_info["category"] = book_category
        book_info["title"] = get_text(page_body.find("h1", id = "bookTitle"))
        book_info["author"] = get_text(page_body.find("span", itemprop="name"))
        book_info["description"] = get_text(page_body.find("div", id="description"))
        book_info["rating"] =  get_text(page_body.find("span", itemprop="ratingValue"))
        book_info["number_of_pages"] = get_text(page_body.find("span", itemprop="numberOfPages"))
        book_info["url"] = url
    return book_info