"""
retriever.py - Handles document retrieval from vector DB
"""

from vector_store.base import query_vector


def default_retriever(vector, top_k=3):
    return query_vector(vector, top_k=top_k)
