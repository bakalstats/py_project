import pickle
import argparse
import pandas as pd
from src.modeling_utils import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classification model training")
    parser.add_argument(
        "--model-file",
        dest="model_file",
        help="model path, usage: --model-file data/clf_model.pkl",
        default="data/clf_model.pkl",
    )
    parser.add_argument(
        "--data-input-file",
        dest="data_input_file",
        default="data/new_data.parquet",
    )
    args = parser.parse_args()
    # upload model
    with open(args.model_file, 'rb') as f:
        multilabel_binarizer, model = pickle.load(f)
    categories = multilabel_binarizer.classes_
    # upload and clean new data
    df = pd.read_parquet(args.data_input_file)
    df = preprocess_data(df, is_training=False)
    # run inference
    y_pred = model.predict_proba(df[TEXT_COL])
    y_pred = [multilabel_predictions(i, CLASSIFICATION_THRESHOLD) for i in y_pred]
    df[CATEGORY_COL] = [[k for j, k in zip(i,categories) if j == 1] for i in y_pred]
    df.to_parquet(args.data_input_file)
