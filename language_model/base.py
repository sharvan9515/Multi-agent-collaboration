from abc import ABC, abstractmethod

class LanguageModel(ABC):
    """Abstract language model interface."""

    @abstractmethod
    def generate(self, messages: list) -> str:
        """Return a model-generated answer for the given messages."""
        pass
