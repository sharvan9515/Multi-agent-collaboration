from celery import Celery
import os
from uuid import uuid4

from embedding.embedder import embed_text
from parsers.text_parser import parse_txt_folder
from vector_store.base import index_document, init_collection
from utils.event_bus import event_bus
from utils.metrics import DOCUMENTS_INGESTED
from storage.audit_log import log_audit_event

broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
app = Celery('rag_tasks', broker=broker_url)

@app.task
def ingest_folder(folder_path: str):
    """Parse text files and index them asynchronously."""
    init_collection()
    docs = parse_txt_folder(folder_path)
    for doc in docs:
        vector = embed_text(doc["text"])
        index_document(
            doc_id=str(uuid4()),
            vector=vector,
            payload={"text": doc["text"], "source": doc["source"]},
        )
        if DOCUMENTS_INGESTED:
            DOCUMENTS_INGESTED.inc()
        log_audit_event("document_ingested", {"source": doc["source"]})
        event_bus.emit("document_ingested", source=doc["source"])
    return len(docs)
