"""
retriever.py - Handles document retrieval from vector DB
"""

from core.vector_store.base import query_vector


def default_retriever(vector, top_k=3, metadata_filter=None):
    """Retrieve documents using vector search and optional metadata filtering."""
    return query_vector(vector, top_k=top_k, filters=metadata_filter)
