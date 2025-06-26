# vector_store/base.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http.exceptions import UnexpectedResponse

COLLECTION_NAME = "claims_collection"
VECTOR_DIMENSION = 384
DISTANCE_METRIC = Distance.COSINE

client = QdrantClient(url="http://localhost:6333")

def init_collection():
    existing = client.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in existing]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_DIMENSION, distance=DISTANCE_METRIC)
        )

def index_document(doc_id, vector, payload):
    client.upsert(
        collection_name=COLLECTION_NAME,
        wait=True,
        points=[{
            "id": doc_id,
            "vector": vector,
            "payload": payload
        }]
    )

def query_vector(vector: list, top_k: int = 5):
    try:
        results = client.search(collection_name=COLLECTION_NAME, query_vector=vector, limit=top_k)
        return results
    except UnexpectedResponse as e:
        raise RuntimeError(f"Query failed: {e}")
