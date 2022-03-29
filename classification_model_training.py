import pickle
import argparse
from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    CountVectorizer,
    ENGLISH_STOP_WORDS,
)
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import hamming_loss, classification_report
from sklearn.pipeline import Pipeline
from src.modeling_utils import *

my_stop_words = ENGLISH_STOP_WORDS


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classification model training")
    parser.add_argument(
        "--model-output-file",
        dest="model_output_file",
        help="model saving path, usage: --model-output-file data/clf_model.pkl",
        default="data/clf_model.pkl",
    )
    # upload training data
    df = upload_data(SCRAPED_DATA_FILE)

    # data preprocessing
    df = preprocess_data(df)

    # model estimation
    multilabel_binarizer = MultiLabelBinarizer()
    multilabel_binarizer.fit(df[LABEL_COL])
    y = multilabel_binarizer.transform(df[LABEL_COL])
    X_train, X_test, y_train, y_test = train_test_split(
        df[TEXT_COL], y, test_size=0.2, random_state=0
    )

    pipe = Pipeline(
        [
            (
                "vct",
                TfidfVectorizer(
                    max_features=20000,
                    sublinear_tf=True,
                    norm="l2",
                    ngram_range=(1, 2),
                    stop_words=my_stop_words,
                ),
            ),
            (
                "clf",
                OneVsRestClassifier(
                    LogisticRegression(random_state=0, solver="lbfgs", C=5)
                ),
            ),
        ]
    )

    model = pipe.fit(X_train, y_train)

    # model performance on test set
    y_pred = model.predict_proba(X_test)
    y_pred = [multilabel_predictions(i, CLASSIFICATION_THRESHOLD) for i in y_pred]
    print(f"Classification report:\n{classification_report(y_test, y_pred)}")
    print(f"Hamming score: {hamming_score(y_test, y_pred)}")
    print(f"Hamming loss: {hamming_loss(y_test, y_pred)}")
    print(f"At least one concurrence score: {single_concurrence_score(y_test, y_pred)}")

    # save model
    args = parser.parse_args()
    with open(args.model_output_file, "wb") as f:
        pickle.dump((multilabel_binarizer, model), f)
