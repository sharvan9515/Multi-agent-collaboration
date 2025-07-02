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
├── agents/                      # Agent implementations
│   ├── base.py                  # Base agent interface
│   └── rag_agent.py             # RAG agent using ChatEngine
├── core/
│   └── workflow.py              # Multi‑agent workflow orchestrator
├── utils/
│   └── logger.py                # Common logging utility
├── embedding/
│   └── embedder.py              # Converts user queries into vector embeddings
├── language_model/
│   └── language_model.py        # GROQ/OpenAI API interface
├── vector_store/
│   └── base.py                  # Qdrant-based vector DB wrapper
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
from vector_store.base import index_document

index_document(
    doc_id=1,
    vector=[0.05] * 384,  # replace with real vector
    payload={"text": "Waiting period for diabetes is 24 months."}
)
```

> 🔜 Coming soon: `scripts/ingest_folder.py` for PDF/text bulk ingestion.

---

## 🤖 Multi-Agent Usage

`MultiAgentCoordinator` lets multiple agents collaborate using a shared
`context` dictionary. Combine the provided `DeidAgent`, `SummaryAgent`, and
`RAGAgent` as needed:

```python
from agents.deid_agent import DeidAgent
from agents.summary_agent import SummaryAgent
from agents.rag_agent import RAGAgent
from core.multi_agent import MultiAgentCoordinator

coordinator = MultiAgentCoordinator([DeidAgent(), SummaryAgent(), RAGAgent()])
response = coordinator.run("Patient John Doe was admitted yesterday.")
```

Each agent receives the current message and can store results in the shared
`context` for the next agent.

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
