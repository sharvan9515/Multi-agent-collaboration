# text_embedding/embedder.py
from sentence_transformers import SentenceTransformer
from .base import EmbeddingModel

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
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed(self, text: str):
        model = self._get_model()
        return model.encode(text)

def embed_text(text: str):
    """Generate a vector embedding for the given text."""
    global _model
    if _model is None:
        _model = SentenceTransformerEmbedder()
    return _model.embed(text)
