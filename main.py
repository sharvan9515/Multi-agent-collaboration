from core.chat_engine.chat_engine import ChatEngine
from core.chat_engine.modules.retriever import default_retriever
from core.chat_engine.modules.prompt_assembler import default_prompt_assembler
from core.embedding.embedder import embed_text
from core.language_model.language_model import generate_answer
from core.vector_store.base import init_collection  # ✅ Make sure this is imported!
from utilities.parsers.text_parser import parse_txt_folder  # ✅ Import parser
from core.vector_store.base import index_document
from uuid import uuid4


def ingest_input_data():
    """Initialize collection and index documents from the input folder."""
    init_collection()
    print("📚 Parsing and indexing text documents from 'input_data/'...")
    docs = parse_txt_folder("input_data/")  # Customize folder path if needed
    for doc in docs:
        vector = embed_text(doc["text"])
        index_document(
            doc_id=str(uuid4()),
            vector=vector,
            payload={"text": doc["text"], "source": doc["source"]},
        )
# main.py - Entry point for the RAG_HEITAA Health Assistant



if __name__ == "__main__":
    ingest_input_data()
    engine = ChatEngine(
        retriever=default_retriever,
        embedder=embed_text,
        llm=generate_answer,
        prompt_assembler=default_prompt_assembler
    )
    print("🩺 Welcome to RAG_HEITAA Health Assistant")
    print("Type 'exit' to end the conversation.\n")
    print("Ask your healthcare question:")

    while True:
        try:
            user_query = input("You: ").strip()

            # Handle empty input
            if not user_query:
                print("⚠️ Please enter a valid question.")
                continue

            if user_query.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break

            answer = engine.answer_query(user_query)
            print(f"\nAssistant: {answer}\n")

        except KeyboardInterrupt:
            print("\n👋 Session ended by user.")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")
