import pandas as pd
import regex as re
from sklearn.feature_extraction.text import (
    ENGLISH_STOP_WORDS,
)
from nltk.stem import PorterStemmer
from src.config import *
my_stop_words = ENGLISH_STOP_WORDS


def clean_text(input_list, stem=False):
    # Text preprocessing
    documents = []
    porter_stemmer = PorterStemmer()

    for input in input_list:
        # Remove all the special characters (needs to be checked)
        document = re.sub(r"\W", " ", input)
        document = document.strip()
        # remove all single characters and numbers
        document = re.sub(r"\s+[a-zA-Z0-9]\s+", " ", document)
        # Remove single characters from the start
        document = re.sub(r"\^[a-zA-Z0-9]\s+", " ", document)
        # Substituting multiple spaces with single space
        document = re.sub(r"\s+", " ", document, flags=re.I)
        # Converting to Lowercase
        document = document.lower()
        # Lemmatization/Stemming
        if stem:
            document = document.split()
            document = [porter_stemmer.stem(word=word) for word in document]
            document = " ".join(document)
        else:
            document = document.split()
            document = " ".join(document)

        documents.append(document)
    return documents


def filter_stop_words(train_sentences, stop_words):
    for i, sentence in enumerate(train_sentences):
        new_sent = [word for word in sentence.split() if word not in stop_words]
        train_sentences[i] = ' '.join(new_sent)
    return train_sentences


def upload_data(path: str):
    df = pd.DataFrame()
    try:
        df = pd.read_parquet(path)
    except FileNotFoundError:
        print("File not found")
    except Exception:
        print("Error")
    return df


def preprocess_data(df: pd.DataFrame, is_training = True):
    if is_training:
        df = (
            df[[TITLE_COL, AUTHOR_COL, DESCRIPTION_COL, CATEGORY_COL]]
            .drop_duplicates()
            .groupby([TITLE_COL, AUTHOR_COL, DESCRIPTION_COL])[CATEGORY_COL]
            .apply(list)
        )
        df = df.reset_index()
    df[AUTHOR_COL] = clean_text(df[AUTHOR_COL], stem=True)
    df[AUTHOR_COL] = [re.sub(" ", "_", text) for text in df[AUTHOR_COL]]
    # Combine all text fields
    df[TEXT_COL] = df[[TITLE_COL, AUTHOR_COL, DESCRIPTION_COL]].agg(' '.join, axis=1)
    # Remove stop words
    df[TEXT_COL] = filter_stop_words(list(df[TEXT_COL]), my_stop_words)
    # Clean text
    df[TEXT_COL] = clean_text(df[TEXT_COL].to_list(), stem=True)
    return df


def hamming_score(y_true, y_pred):
    return (
        (y_true & y_pred).sum(axis=1) / (y_true | y_pred).sum(axis=1)
    ).mean()


def multilabel_predictions(y_pred, threshold):
    result = [1 if j >= threshold else 0 for j in y_pred]
    if not any(result):
        idx = list(y_pred).index(max(y_pred))
        result[idx] = 1
    return result


def single_concurrence_score(y_true, y_pred):
    return (
            (y_true & y_pred).any(axis=1)
    ).mean()