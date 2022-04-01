import pickle
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.calibration import CalibratedClassifierCV
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
    parser.add_argument(
        "--show-model-performace",
        dest="show_model_performance",
        default=True,
    )
    args = parser.parse_args()

    df = upload_data(SCRAPED_DATA_FILE)
    df, y, multilabel_binarizer = preprocess_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        df[TEXT_COL], y, test_size=TEST_SET_SHARE, random_state=0
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

    if args.show_model_performance:
        model_performance = evaluate_model_performance(model, X_test, y_test)
        print(model_performance)

    save_model(multilabel_binarizer, model, args.model_output_file)
