"""
chat_engine.py - Orchestrates the RAG process: embedding, retrieval, and generation
"""
from chat_engine.modules.session import ChatSession

from embedding.embedder import embed_text
from vector_store.base import query_vector
from language_model.language_model import generate_answer


class ChatEngine:
    def __init__(self, retriever, embedder, llm, prompt_assembler):
        self.retriever = retriever
        self.embedder = embedder
        self.llm = llm
        self.prompt_assembler = prompt_assembler
        self.session = ChatSession()

    def answer_query(self, user_query: str) -> str:

        self.session.add_user_message(user_query)
        # Step 1: Embed user query
        query_vec = self.embedder(user_query)

        # Step 2: Retrieve top documents
        results = self.retriever(query_vec, top_k=3)
        history = self.session.get_recent_history()
        

        # Step 3: Assemble context from retrieved documents
        context_snippets = []
        for res in results:
            if res.payload and "text" in res.payload:
                context_snippets.append(res.payload["text"])
        context_text = "\n\n".join(context_snippets)

        # Step 4: Build final prompt and generate answer
        prompt = self.prompt_assembler(user_query, context_text,history)
        response = self.llm(prompt)
        self.session.add_assistant_message(response)
        return response
