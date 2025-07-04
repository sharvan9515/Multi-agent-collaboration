import argparse

from core.embedding.embedder import embed_text
from utilities.parsers.text_parser import parse_txt_folder
from core.vector_store.base import init_collection, index_document
from uuid import uuid4


def ingest_folder(folder_path: str):
    """Parse text files in ``folder_path`` and index them in the vector store."""
    init_collection()
    docs = parse_txt_folder(folder_path)
    for doc in docs:
        vector = embed_text(doc["text"])
        index_document(doc_id=str(uuid4()), vector=vector,
                       payload={"text": doc["text"], "source": doc["source"]})


def main():
    parser = argparse.ArgumentParser(
        description="Ingest all .txt files from a folder into Qdrant")
    parser.add_argument("folder", help="Path to folder containing text files")
    args = parser.parse_args()
    ingest_folder(args.folder)


if __name__ == "__main__":
    main()
