from abc import ABC, abstractmethod

class EmbeddingModel(ABC):
    """Abstract base class for embedding models."""

    @abstractmethod
    def embed(self, text: str):
        """Return the vector representation for the given text."""
        pass
