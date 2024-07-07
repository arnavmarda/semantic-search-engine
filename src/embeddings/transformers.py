from sentence_transformers import SentenceTransformer

# from sentence_transformers.quantization import (
#     semantic_search_usearch,
#     quantize_embeddings,
# )
# from math import ceil
# from rich.pretty import pprint

# from sentence_transformers.util import semantic_search

MPNET_BASE = "sentence-transformers/multi-qa-mpnet-base-cos-v1"  # 170 queries/sec
DISTILBERT = "sentence-transformers/multi-qa-distilbert-cos-v1"  # 350 queries/sec
MINILM = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"  # 750 queries/sec

model = SentenceTransformer(DISTILBERT)


def embed_query(query):
    """
    Returns vector embedding of query.
    """
    return model.encode(query, normalize_embeddings=True)


def embed_corpus_text(text: list):
    """
    Returns vector embeddings of text.
    """
    if len(text) == 0:
        print("Error in embed_corpus_text: Empty text list!")
        return []
    return model.encode(text, normalize_embeddings=True)


def link_similarity(query, corpus_text):
    """
    Returns similarity score between query and corpus text.
    """
    if len(corpus_text) == 0:
        return 0
    query_embedding = embed_query(query)
    corpus_embedding = embed_corpus_text(corpus_text)
    similary = model.similarity(query_embedding, corpus_embedding)
    return round(sum(similary[0]).item() / len(corpus_text), 3)
