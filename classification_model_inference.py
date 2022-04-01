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
    multilabel_binarizer, model = upload_model(args.model_file)
    df = upload_data(args.data_input_file)
    df = preprocess_data(df, is_training=False)
    df = predict_categories(model, df, multilabel_binarizer.classes_)
    df.to_parquet(args.data_input_file)
