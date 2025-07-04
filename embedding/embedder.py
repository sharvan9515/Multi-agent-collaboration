# text_embedding/embedder.py
try:
    from sentence_transformers import SentenceTransformer
except ImportError:  # pragma: no cover - optional dependency
    SentenceTransformer = None
from .base import EmbeddingModel
try:
    import numpy as np
except ImportError:  # pragma: no cover - optional dependency
    np = None

# Choose embedding model: MiniLM (fast) or BioBERT (domain-specific)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# For BioBERT, one could use a HuggingFace model like "pritamdeka/BioBERT-mnli-snli" or similar if available

_model = None


class SentenceTransformerEmbedder(EmbeddingModel):
    """Pluggable embedder based on SentenceTransformer."""

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model_name = model_name
        self._model = None

    def _get_model(self):
        if self._model is None and SentenceTransformer is not None:
            try:
                self._model = SentenceTransformer(self.model_name)
            except Exception as e:  # pragma: no cover - model download failure
                print(
                    f"⚠️ Unable to load embedding model '{self.model_name}': {e}"
                )
                print("   Falling back to deterministic random embeddings.")
                self._model = None
        return self._model

    def embed(self, text: str):
        model = self._get_model()
        if model is None:
            # Deterministic random vector based on text hash
            if np is not None:
                rng = np.random.RandomState(abs(hash(text)) % (2**32))
                return rng.rand(384).tolist()
            import random
            random.seed(abs(hash(text)) % (2**32))
            return [random.random() for _ in range(384)]
        return model.encode(text).tolist()

def embed_text(text: str):
    """Generate a vector embedding for the given text."""
    global _model
    if _model is None:
        _model = SentenceTransformerEmbedder()
    return _model.embed(text)
