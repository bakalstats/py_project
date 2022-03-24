# This could be main part of the project

page_urls = handle_category()
book_urls = get_book_urls(page_urls)
books_data = get_books_data(book_urls)



# Consider using yield for each url, instead of returning whole list
def get_book_urls():
    # Get response
    # Parse response
    # Return data


# Consider using yield for each item, instead of returning whole list
def get_books_data():
    # Get response
    # Parse response
    # Return data

books_db = pd.DataFrame(books_data)
books_db.to_parquet("books_info.parquet")
