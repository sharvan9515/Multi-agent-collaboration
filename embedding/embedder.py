# text_embedding/embedder.py
from sentence_transformers import SentenceTransformer
import os
import torch

# Choose embedding model: MiniLM (fast) or BioBERT (domain-specific)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# For BioBERT, one could use a HuggingFace model like "pritamdeka/BioBERT-mnli-snli" or similar if available

# Force all operations on CPU for broad compatibility
torch.set_num_threads(os.cpu_count())
model = SentenceTransformer(EMBEDDING_MODEL, device="cpu")

def embed_text(text: str):
    """Generate a vector embedding for the given text."""
    # Ensure text is a string (or a list of strings if batch)
    return model.encode(text)
