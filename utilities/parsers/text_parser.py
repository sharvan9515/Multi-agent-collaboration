import os
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter

def parse_txt_folder(folder_path: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List[Dict]:
    """
    Parse .txt files in a folder and split into chunks using LangChain's RecursiveCharacterTextSplitter.
    Returns list of dicts: {"text": chunk, "source": filename}
    """
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
                chunks = splitter.split_text(text)
                for chunk in chunks:
                    documents.append({
                        "text": chunk.strip(),
                        "source": filename
                    })
    return documents
