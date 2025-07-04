"""Chat engine orchestration logic.

The original implementation imported heavy dependencies at module import time.
This made it impossible to import :class:`ChatEngine` when optional packages
(like ``sentence_transformers``) were missing.  To keep the module lightweight,
we now load the default components lazily when no custom implementations are
provided.
"""

from chat_engine.modules.session import ChatSession
from utils.event_bus import event_bus
from utils.metrics import AGENT_RUNS
from storage.audit_log import log_audit_event


class ChatEngine:
    def __init__(
        self,
        retriever=None,
        embedder=None,
        llm=None,
        prompt_assembler=None,
    ):
        """Create a new ``ChatEngine`` instance.

        Parameters are optional.  When omitted we lazily import lightweight
        defaults, avoiding heavy dependencies when the engine is used in unit
        tests or simple scripts.
        """

        if retriever is None:
            from .modules.retriever import default_retriever

            retriever = default_retriever
        if embedder is None:
            from embedding.embedder import embed_text

            embedder = embed_text
        if llm is None:
            from language_model.language_model import generate_answer

            llm = generate_answer
        if prompt_assembler is None:
            from .modules.prompt_assembler import default_prompt_assembler

            prompt_assembler = default_prompt_assembler

        self.retriever = retriever
        self.embedder = embedder
        self.llm = llm
        self.prompt_assembler = prompt_assembler
        self.session = ChatSession()

    def answer_query(self, user_query: str) -> str:
        self.session.add_user_message(user_query)
        event_bus.emit("chat_message_received", message=user_query)
        # Step 1: Embed user query
        query_vec = self.embedder(user_query)

        # Step 2: Retrieve top documents
        results = self.retriever(query_vec, top_k=3)
        history = self.session.get_recent_history()

        if not results:
            warning = "\u26a0\ufe0f I'm unable to locate relevant information."
            self.session.add_assistant_message(warning)
            log_audit_event("chat", {"question": user_query, "answer": warning})
            event_bus.emit("chat_response_generated", response=warning)
            return warning

        # Step 3: Assemble context from retrieved documents
        context_snippets = []
        for res in results:
            if res.payload and "text" in res.payload:
                context_snippets.append(res.payload["text"])
        context_text = "\n\n".join(context_snippets)

        # Step 4: Build final prompt and generate answer
        prompt = self.prompt_assembler(user_query, context_text, history)
        response = self.llm(prompt)
        self.session.add_assistant_message(response)
        if AGENT_RUNS:
            AGENT_RUNS.labels(agent="ChatEngine").inc()
        log_audit_event("chat", {"question": user_query, "answer": response})
        event_bus.emit("chat_response_generated", response=response)
        return response
