# question_answering/rag_qa.py
from embedding.embedder import embed_text
from vector_store.base import query_vector
from language_model.language_model import generate_answer

def answer_query(user_query: str) -> str:
    """Retrieve relevant contexts for the query and get an answer from the language model."""
    # 1. Embed the user query
    query_vec = embed_text(user_query)
    # 2. Retrieve top relevant documents from Qdrant
    results = query_vector(query_vec, top_k=3)
    # 3. Build context string from retrieved results
    context_snippets = []
    for res in results:
        # Assuming payload contains the text of the claim
        if res.payload and "text" in res.payload:
            context_snippets.append(res.payload["text"])
    context_text = "\n\n".join(context_snippets)
    # 4. Create a prompt for the LLM that includes the context
    prompt = (f"You are a healthcare claims assistant. Use the following claim records as context to answer the question.\n"
              f"Context:\n{context_text}\n\nQuestion: {user_query}\nAnswer:")
    # 5. Generate answer using OpenAI model
    answer = generate_answer(prompt)
    return answer
