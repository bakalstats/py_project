import pandas as pd
import regex as re
import numpy as np
import pickle
from sklearn.feature_extraction.text import (
    ENGLISH_STOP_WORDS,
)
from sklearn.metrics import hamming_loss, classification_report
from sklearn.preprocessing import MultiLabelBinarizer
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


def preprocess_data(df: pd.DataFrame, is_training=True):
    y = None
    if is_training:
        df = (
            df[[TITLE_COL, AUTHOR_COL, DESCRIPTION_COL, CATEGORY_COL]]
            .drop_duplicates()
            .groupby([TITLE_COL, AUTHOR_COL, DESCRIPTION_COL])[CATEGORY_COL]
            .apply(list)
        )
        df = df.reset_index()

        binarizer = MultiLabelBinarizer()
        binarizer.fit(df[LABEL_COL])
        y = binarizer.transform(df[LABEL_COL])

    df[AUTHOR_COL] = clean_text(df[AUTHOR_COL], stem=True)
    df[AUTHOR_COL] = [re.sub(" ", "_", text) for text in df[AUTHOR_COL]]
    # Combine all text fields
    df[TEXT_COL] = df[[TITLE_COL, AUTHOR_COL, DESCRIPTION_COL]].agg(' '.join, axis=1)
    # Remove stop words
    df[TEXT_COL] = filter_stop_words(list(df[TEXT_COL]), my_stop_words)
    # Clean text
    df[TEXT_COL] = clean_text(df[TEXT_COL].to_list(), stem=True)
    return df, y, binarizer


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


def book_search(query, df, model, top_k=3):
    query_embedding = model.encode([query])
    df[DISTANCE_COL] = [np.linalg.norm(query_embedding - i) for i in df[EMBEDDINGS_COL]]
    search_result = df.sort_values([DISTANCE_COL], ascending=False).head(top_k)
    return search_result[[TITLE_COL, AUTHOR_COL, DESCRIPTION_COL, CATEGORY_COL]]


def search_data_preprocess(df):
    df = (
        df[[TITLE_COL, AUTHOR_COL, DESCRIPTION_COL, CATEGORY_COL]]
        .drop_duplicates()
        .groupby([TITLE_COL, AUTHOR_COL, DESCRIPTION_COL])[CATEGORY_COL]
        .apply(lambda x: ", ".join(x))
    )
    df = df.reset_index()
    df[TEXT_COL] = df[[CATEGORY_COL, AUTHOR_COL, TITLE_COL, DESCRIPTION_COL]].agg(
        " ".join, axis=1
    )
    return df


def predict_categories(model, df, categories):
    y_pred = model.predict_proba(df[TEXT_COL])
    y_pred = [multilabel_predictions(i, CLASSIFICATION_THRESHOLD) for i in y_pred]
    df[CATEGORY_COL] = [[k for j, k in zip(i,categories) if j == 1] for i in y_pred]
    return df


def upload_model(path):
    with open(path, 'rb') as f:
        multilabel_binarizer, model = pickle.load(f)
    return multilabel_binarizer, model


def save_model(binarizer, model, model_output_file):
    with open(model_output_file, "wb") as f:
        pickle.dump((binarizer, model), f)


def evaluate_model_performance(model, X_test, y_test):
    model_performace_summary = {}
    y_pred = model.predict_proba(X_test)
    y_pred = [multilabel_predictions(i, CLASSIFICATION_THRESHOLD) for i in y_pred]
    model_performace_summary["Classification report"] = classification_report(y_test, y_pred)
    model_performace_summary["Hamming score"] = hamming_score(y_test, y_pred)
    model_performace_summary["Hamming loss"] = hamming_loss(y_test, y_pred)
    model_performace_summary["At least one concurrence score"] = single_concurrence_score(y_test, y_pred)
    return model_performace_summary
