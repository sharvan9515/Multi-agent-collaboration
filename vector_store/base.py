# vector_store/base.py
from abc import ABC, abstractmethod
import logging
import os

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams
    from qdrant_client.http.exceptions import UnexpectedResponse
    from qdrant_client.http.models import PointStruct
except ImportError:  # pragma: no cover - optional dependency
    QdrantClient = None
    Distance = None
    VectorParams = None
    UnexpectedResponse = Exception
    PointStruct = None

COLLECTION_NAME = "claims_collection"
VECTOR_DIMENSION = 384
DISTANCE_METRIC = Distance.COSINE if Distance else None

logger = logging.getLogger(__name__)

QDRANT_URL = os.getenv("QDRANT_URL")

def _create_client():
    """Create a Qdrant client if available and reachable."""

    if QdrantClient is None:
        logger.warning("qdrant_client not installed; falling back to in-memory store")
        return None

    if not QDRANT_URL:
        logger.warning("QDRANT_URL not set, using in-memory instance")
        return QdrantClient(location=":memory:")

    try:
        client = QdrantClient(url=QDRANT_URL)
        # Trigger a simple request to verify connectivity
        client.get_collections()
        return client
    except Exception:
        logger.warning("Could not connect to Qdrant at %s, using in-memory instance", QDRANT_URL)
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


class InMemoryVectorStore(VectorStore):
    """Simple in-memory fallback when qdrant_client is unavailable."""

    def __init__(self):
        self._data = []  # List of (id, vector, payload)

    def init_collection(self):
        pass  # Nothing to initialize

    def index_document(self, doc_id, vector, payload):
        self._data.append((doc_id, vector, payload))

    def _similarity(self, v1, v2):
        try:
            import numpy as np
        except ImportError:  # pragma: no cover - optional dependency
            np = None

        if np is not None:
            v1 = np.array(v1)
            v2 = np.array(v2)
            denom = (np.linalg.norm(v1) * np.linalg.norm(v2)) or 1.0
            return float(np.dot(v1, v2) / denom)
        # Basic Python fallback (cosine similarity)
        import math

        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        denom = (norm1 * norm2) or 1.0
        return float(dot / denom)

    def query_vector(self, vector, top_k: int = 5, filters=None):
        scored = [
            (self._similarity(vector, v), payload)
            for _, v, payload in self._data
        ]
        scored.sort(key=lambda x: x[0], reverse=True)

        class DummyResult:
            def __init__(self, payload):
                self.payload = payload

        return [DummyResult(p) for _, p in scored[:top_k]]


# Instantiate a default store for convenience
_default_store = QdrantVectorStore() if QdrantClient else InMemoryVectorStore()

def init_collection():
    _default_store.init_collection()

def index_document(doc_id, vector, payload):
    _default_store.index_document(doc_id, vector, payload)

def query_vector(vector: list, top_k: int = 5, filters=None):
    return _default_store.query_vector(vector, top_k=top_k, filters=filters)
