import argparse
from sentence_transformers import SentenceTransformer
from src.modeling_utils import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Semantic search model")
    parser.add_argument(
        "--data-input-file",
        dest="data_input_file",
        default="data/goodreads_data.parquet",
    )
    args = parser.parse_args()

    # Fully pre-trained model at the current stage
    model = SentenceTransformer(PRETRAINED_SEMANTIC_SEARCH_MODEL)
    model.save(LOCAL_SEARCH_MODEL_PATH)

    df = upload_data(args.data_input_file)
    df = search_data_preprocess(df)
    books_embeddings = model.encode(df[TEXT_COL].tolist())
    df[EMBEDDINGS_COL] = list(books_embeddings)
    df.to_parquet(DATA_EMBEDDINGS_FILE)
