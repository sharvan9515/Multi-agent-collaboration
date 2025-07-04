from core.chat_engine.chat_engine import ChatEngine
from core.chat_engine.modules.retriever import default_retriever
from core.chat_engine.modules.prompt_assembler import default_prompt_assembler
from core.embedding.embedder import embed_text
from core.language_model.language_model import generate_answer

from .base import Agent


class RAGAgent(Agent):
    """Agent that answers questions using the RAG ChatEngine."""

    def __init__(self):
        self.engine = ChatEngine(
            retriever=default_retriever,
            embedder=embed_text,
            llm=generate_answer,
            prompt_assembler=default_prompt_assembler,
        )

    def act(self, message: str, context: dict) -> tuple[str, dict]:
        """Answer a question and append the response to context messages."""
        response = self.engine.answer_query(message)
        context.setdefault("messages", []).append({"role": "assistant", "content": response})
        return response, context
