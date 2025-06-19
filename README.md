# 🧠 RAG_HEITAA – Context-Aware RAG System for Healthcare & Insurance Claims

RAG_HEITAA is a **modular, production-ready Retrieval-Augmented Generation (RAG)** system designed for healthcare and insurance claims automation. It integrates a local or cloud-based vector database (Qdrant) with LLMs (via GROQ API), supporting chat history awareness, dynamic prompt construction, and easy backend extensibility.

---

## 🔧 Features

✅ Context-aware, multi-turn healthcare Q&A  
✅ Modular vector store layer (Qdrant by default, extendable to Pinecone, FAISS, etc.)  
✅ GROQ OpenAI-compatible LLM support  
✅ Clean plug-and-play ingestion and retrieval interface  
✅ Pythonic `ChatEngine` orchestrator  

---

## 📁 Project Structure

```
RAG_HEITAA/
├── chat_engine/
│   ├── chat_engine.py           # Orchestrates RAG flow
│   └── modules/
│       ├── prompt_assembler.py  # Builds prompts from chat + retrieved docs
│       ├── retriever.py         # Vector-based document retriever
│       └── session.py           # Maintains multi-turn chat history
├── embedding/
│   └── embedder.py              # Converts user queries into vector embeddings
├── language_model/
│   └── lm.py                    # GROQ/OpenAI API interface
├── vector_search_engine/
│   └── vector_store.py          # Qdrant-based vector DB wrapper
├── main.py                      # Entry point CLI chatbot
└── .env                         # API keys for GROQ (not committed)
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/RAG_HEITAA.git
cd RAG_HEITAA
```

### 2. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Set Your API Key

Create a `.env` file in the root folder:

```ini
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Start Qdrant

You can use local Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Or use [Qdrant Cloud](https://qdrant.tech/).

---

## 🧠 How It Works

1. **Query Embedding**  
   → `embed_text()` encodes user input into a vector.

2. **Vector Retrieval**  
   → `query_vector()` searches Qdrant for similar claims-related documents.

3. **Prompt Construction**  
   → `prompt_assembler()` builds a chat-aware prompt with history + knowledge.

4. **LLM Response**  
   → `generate_answer()` calls the GROQ API to return a grounded answer.

5. **Session Tracking**  
   → `ChatSession` stores previous turns to enable follow-up questions.

---

## ✅ Run the Chatbot

```bash
python main.py
```

Then type your question:

```text
You: What is the waiting period for diabetes?
Assistant: The waiting period for diabetes is typically...
```

---

## 📦 Ingesting New Documents

To add documents to Qdrant:

```python
from vector_search_engine.vector_store import index_document

index_document(
    doc_id=1,
    vector=[0.05] * 384,  # replace with real vector
    payload={"text": "Waiting period for diabetes is 24 months."}
)
```

> 🔜 Coming soon: `scripts/ingest_folder.py` for PDF/text bulk ingestion.

---

## 🧪 Testing

You can manually test:
```bash
python -c "from language_model.lm import generate_answer; print(generate_answer([...]))"
```

Or run `main.py` and ask natural questions.

---

## 🔄 Extensibility

- Swap vector store in `vector_store/base.py` with FAISS/Pinecone.
- Switch from GROQ to OpenAI or Claude by modifying `lm.py`.
- Add Streamlit/Gradio frontend easily using `ChatEngine`.

---

## 🤝 Contributing

1. Fork this repo  
2. Create your feature branch (`git checkout -b feature/chat-ui`)  
3. Commit your changes  
4. Push to your branch (`git push origin feature/chat-ui`)  
5. Open a Pull Request  

---

## 🛡️ License

MIT License © 2024 Vittala Sharvan
