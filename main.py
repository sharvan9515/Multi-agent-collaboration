from chat_engine.chat_engine import ChatEngine
from chat_engine.modules.retriever import default_retriever
from chat_engine.modules.prompt_assembler import default_prompt_assembler
from embedding.embedder import embed_text
from language_model.language_model import generate_answer
from vector_store.base import init_collection  # ✅ Make sure this is imported!


init_collection()

if __name__ == "__main__":
    engine = ChatEngine(
        retriever=default_retriever,
        embedder=embed_text,
        llm=generate_answer,
        prompt_assembler=default_prompt_assembler
    )
    print("🩺 Welcome to RAG_HEITAA Health Assistant")
    print("Type 'exit' to end the conversation.\n")
    print("Ask your healthcare question:")
    print("🩺 Welcome to RAG_HEITAA Health Assistant")
    print("Type 'exit' to end the conversation.\n")

    while True:
        user_query = input("You: ")
        if user_query.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        answer = engine.answer_query(user_query)
        print(f"\nAssistant: {answer}\n")

