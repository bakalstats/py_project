# py_project

Action points:
- Create script for scraping books information of interest: Title, Author, Description, Rating, Number of pages. www.goodreads.com is used as an test example. 
  - Done via BeautifulSoup. Rather slow for scraping the whole site, worth trying Scrapy.
  - Data scraped for about 10 categories only (takes rather long).
  - Script was re-formed from notebook to separate py files and slightly refactored.

- Create classification model to identify book category based on description.
  - Multilabel classification model training and inference steps were created based on logistic regression using Sklearn
  - Worth trying TF DNN approach and/or more tune hyper parameters

To do (depending on time availability):
- Try book search/recomendation based on short description/request.
