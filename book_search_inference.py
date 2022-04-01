import argparse
from sentence_transformers import SentenceTransformer
from src.modeling_utils import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Semantic search model inference")
    parser.add_argument(
        "--query",
        dest="query",
        default="bestseller novel with true heros",
    )
    parser.add_argument(
        "--use-local-model",
        dest="use_local_model",
        default=True,
    )
    parser.add_argument(
        "--topk",
        dest="top_k",
        default=3,
    )
    args = parser.parse_args()
    df = upload_data(DATA_EMBEDDINGS_FILE)
    if args.use_local_model:
        model = SentenceTransformer(LOCAL_SEARCH_MODEL_PATH)
    else:
        model = SentenceTransformer(PRETRAINED_SEMANTIC_SEARCH_MODEL)

    top_search_results = book_search(args.query, df, model, args.top_k)
    print(top_search_results)
