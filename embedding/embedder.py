# text_embedding/embedder.py
from sentence_transformers import SentenceTransformer
from .base import EmbeddingModel
import numpy as np

# Choose embedding model: MiniLM (fast) or BioBERT (domain-specific)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# For BioBERT, one could use a HuggingFace model like "pritamdeka/BioBERT-mnli-snli" or similar if available

_model = None


class SentenceTransformerEmbedder(EmbeddingModel):
    """Pluggable embedder based on SentenceTransformer."""

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model_name = model_name
        self._model = None

    def _get_model(self) -> SentenceTransformer:
        if self._model is None:
            try:
                self._model = SentenceTransformer(self.model_name)
            except Exception as e:
                print(
                    f"⚠️ Unable to load embedding model '{self.model_name}': {e}"\
                )
                print("   Falling back to deterministic random embeddings.")
                self._model = None
        return self._model

    def embed(self, text: str):
        model = self._get_model()
        if model is None:
            # Deterministic random vector based on text hash
            rng = np.random.RandomState(abs(hash(text)) % (2**32))
            return rng.rand(384).tolist()
        return model.encode(text).tolist()

def embed_text(text: str):
    """Generate a vector embedding for the given text."""
    global _model
    if _model is None:
        _model = SentenceTransformerEmbedder()
    return _model.embed(text)
