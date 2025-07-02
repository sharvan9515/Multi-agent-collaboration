# vector_store/base.py
from abc import ABC, abstractmethod
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import PointStruct
import os

COLLECTION_NAME = "claims_collection"
VECTOR_DIMENSION = 384
DISTANCE_METRIC = Distance.COSINE

QDRANT_URL = os.getenv("QDRANT_URL")

def _create_client():
    """Create a Qdrant client. Fall back to in-memory instance if the server is
    unreachable or no URL is provided."""

    if not QDRANT_URL:
        # Default to in-memory instance when no URL is specified
        return QdrantClient(location=":memory:")

    try:
        client = QdrantClient(url=QDRANT_URL)
        # Trigger a simple request to verify connectivity
        client.get_collections()
        return client
    except Exception:
        # Gracefully fall back to in-memory instance
        print(f"⚠️ Could not connect to Qdrant at {QDRANT_URL}, using in-memory instance")
        return QdrantClient(location=":memory:")


client = _create_client()


class VectorStore(ABC):
    """Abstract vector store interface."""

    @abstractmethod
    def init_collection(self):
        pass

    @abstractmethod
    def index_document(self, doc_id, vector, payload):
        pass

    @abstractmethod
    def query_vector(self, vector, top_k: int = 5, filters=None):
        pass


class QdrantVectorStore(VectorStore):
    """Qdrant-backed vector store implementation."""

    def init_collection(self):
        existing = client.get_collections().collections
        if COLLECTION_NAME not in [c.name for c in existing]:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=VECTOR_DIMENSION, distance=DISTANCE_METRIC),
            )

    def index_document(self, doc_id, vector, payload):
        point = PointStruct(id=doc_id, vector=vector, payload=payload)
        client.upsert(
            collection_name=COLLECTION_NAME,
            wait=True,
            points=[point],
        )

    def query_vector(self, vector: list, top_k: int = 5, filters=None):
        try:
            results = client.search(
                collection_name=COLLECTION_NAME,
                query_vector=vector,
                limit=top_k,
                query_filter=filters,
            )
            return results
        except UnexpectedResponse as e:
            raise RuntimeError(f"Query failed: {e}")


# Instantiate a default store for convenience
_default_store = QdrantVectorStore()

def init_collection():
    _default_store.init_collection()

def index_document(doc_id, vector, payload):
    _default_store.index_document(doc_id, vector, payload)

def query_vector(vector: list, top_k: int = 5, filters=None):
    return _default_store.query_vector(vector, top_k=top_k, filters=filters)
