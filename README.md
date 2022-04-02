# py_project

Action points:
- Create script for scraping books information of interest: Title, Author, Description, Rating, Number of pages. www.goodreads.com was chosen for experiments.
    - Done via BeautifulSoup. Rather slow for scraping the whole site, worth trying Scrapy.
    - For the further experiments scraped only top 5 pages with books per about 10 first categories

| category|  book_count|
| ----------- | ----------- |
|children   |      498|
|fantasy  |       494|
|fiction  |       495|
|history |        498|
|horror   |      500|
|mystery  |       498|
|non-fiction |        498|
|romance   |      499|
|science-fiction  |       279|
|young-adult  |       506|

- Create classification model to identify book category based on it's title, author and description.
    - Multilabel classification model was created (both training and inference steps) based on sklearn logistic regression. 
    - Model performance is rather moderate, worth trying to tune some parameters or try using DNN architecture.

- Create semantic book search based on short queries/requests.
    - At the current stage semantic search is implemented via fully pre-trained SBERT model
    - To do: Fine tune model for better search results
