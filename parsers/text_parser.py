import os
from typing import List, Dict
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ImportError:  # pragma: no cover - optional dependency
    RecursiveCharacterTextSplitter = None

def parse_txt_folder(folder_path: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List[Dict]:
    """
    Parse .txt files in a folder and split into chunks using LangChain's RecursiveCharacterTextSplitter.
    Returns list of dicts: {"text": chunk, "source": filename}
    """
    if RecursiveCharacterTextSplitter is None:
        def _split(text):
            chunks = []
            for i in range(0, len(text), chunk_size):
                chunks.append(text[i : i + chunk_size])
            return chunks
        splitter = None
    else:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                text = f.read()
                if splitter is None:
                    chunks = _split(text)
                else:
                    chunks = splitter.split_text(text)
                for chunk in chunks:
                    documents.append({
                        "text": chunk.strip(),
                        "source": filename
                    })
    return documents
