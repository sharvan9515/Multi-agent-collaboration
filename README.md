# 🧠 RAG_HEITAA – Context-Aware RAG System for Healthcare & Insurance Claims

RAG_HEITAA is a **modular, production-ready Retrieval-Augmented Generation (RAG)** system designed for healthcare and insurance claims automation. It integrates a local or cloud-based vector database (Qdrant) with LLMs (via GROQ API), supporting chat history awareness, dynamic prompt construction, and easy backend extensibility.

---

## 🔧 Features

✅ Context-aware, multi-turn healthcare Q&A  
✅ Modular vector store layer (Qdrant by default, extendable to Pinecone, FAISS, etc.)  
✅ GROQ OpenAI-compatible LLM support  
✅ Clean plug-and-play ingestion and retrieval interface
✅ Pythonic `ChatEngine` orchestrator
✅ Pluggable embeddings/LLMs/vector stores
✅ Multi-strategy retrieval with metadata filters
✅ Versioned REST & GraphQL API with token auth

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
├── api/                         # FastAPI server
│   └── app.py                   # REST & GraphQL endpoints
├── frontend/                    # Voice chat UI
│   └── index.html
├── async_tasks/                 # Celery tasks
│   └── tasks.py
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

**Windows note:** The `tokenizers` package may fail to build from source on
some Rust toolchains. If this happens, install the precompiled wheel with:

```bash
pip install tokenizers --prefer-binary
```

The `requirements.txt` file already pins a compatible version
(`tokenizers==0.13.3`) to avoid these build issues.

If the SentenceTransformer model cannot be downloaded (e.g. when running
offline), the application will fall back to deterministic random embeddings so
that you can still test the pipeline.

### 3. Set Your API Key

Create a `.env` file in the root folder:

```ini
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

If this key is missing or the Groq API is unreachable, RAG_HEITAA will
automatically respond with a simple offline model so you can still test
the workflow.

### 4. Start Qdrant

You can use local Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Or use [Qdrant Cloud](https://qdrant.tech/).

### 🐳 Docker Compose

A `docker-compose.yml` is provided to launch the app together with a Qdrant
service. Build and start both containers with:

```bash
docker compose up --build
```

The application container will connect to the `qdrant` service automatically
using the `QDRANT_URL` environment variable. If this variable is not set or the
server cannot be reached, RAG_HEITAA will automatically start an in-memory
Qdrant instance for local development.

### 5. Run the Application

Launch the chatbot from the command line:

```bash
python main.py
```

Or start the API server and open `http://localhost:8000` in your browser:

```bash
uvicorn api.app:app --reload
```

### 🚀 Async Ingestion
Start a Celery worker to process heavy ingestion jobs. The broker URL can be
overridden with the `CELERY_BROKER_URL` environment variable (defaults to
`redis://redis:6379/0`):
```bash
celery -A async_tasks.tasks worker --loglevel=info
```
Make sure a Redis instance is accessible at the broker URL, e.g. start one with:
```bash
docker run -p 6379:6379 redis
```


---

## 🧠 How It Works

1. **Query Embedding**  
   → `embed_text()` encodes user input into a vector.

2. **Vector Retrieval**  
   → `query_vector()` searches Qdrant for similar claims-related documents.

3. **Prompt Construction**  
   → `prompt_assembler()` builds a chat-aware prompt with history + knowledge.

4. **LLM Response**  
   → `generate_answer()` normally calls the GROQ API. If that fails or
     no API key is configured, a simple offline echo model responds instead.

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

For bulk ingestion of a folder of `.txt` files:

```bash
python scripts/ingest_folder.py path/to/folder
```

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

For more dynamic control you can use ``LLMSupervisor`` which relies on a
language model to pick the next agent based on the conversation so far.
It automatically discovers agents from the ``agents`` package and lets you
register new ones programmatically:

```python
from core import LLMSupervisor

supervisor = LLMSupervisor.from_package()
reply = supervisor.run("Summarize and anonymize this report")
```

If you need a smarter orchestrator that can summarize long histories and
prevent runaway loops, use ``AdvancedSupervisor``:

```python
from core import AdvancedSupervisor

supervisor = AdvancedSupervisor.from_package(max_turns=5)
result = supervisor.run("Encrypt then summarize this document")
```

### Workflow Hooks & Events

Workflows can trigger custom hooks before and after each agent runs. Subscribe
to the `event_bus` to react to `workflow_start`, `agent_end`, or other events.
Metrics are exposed via optional Prometheus counters in `utils.metrics`.

## 🔒 Cybersecurity Agent

The repository includes a `SecurityAgent` that validates message integrity and
checks service health. It relies on the helpers in the `cybersecurity/`
directory:

- `encryption.py` – symmetric encryption based on Fernet.
- `integrity.py` – SHA‑256 hashing utilities.
- `monitor.py` – simple checks for Qdrant and the message broker.

### Setup

1. Install the optional dependency:
   ```bash
   pip install cryptography
   ```
2. Generate an encryption key and store it in the `ENCRYPTION_KEY` variable:
   ```bash
   python -c "from cybersecurity.encryption import generate_key; generate_key()"
   ```

### Usage

Add the agent to your workflow so incoming messages are decrypted and verified
before other agents run:

```python
from agents.security_agent import SecurityAgent
from agents.rag_agent import RAGAgent
from core.multi_agent import MultiAgentCoordinator

coordinator = MultiAgentCoordinator([SecurityAgent(), RAGAgent()])
result, ctx = coordinator.run(encrypted_message, {"hash": expected_hash})
```

The agent decrypts the input, verifies the hash when provided, checks that
Qdrant and Redis are reachable, and then re‑encrypts the output.

---

## 🔌 API Server

Start the FastAPI server with GraphQL and REST endpoints:

```bash
uvicorn api.app:app --reload
```

After starting the server, open `http://localhost:8000/` in your browser to use
the bundled HTML demo. Authenticate requests using the `API_TOKEN`
environment variable. Endpoints are versioned under `/v1`.

## 🖥️ Streamlit Frontend

For a more convenient UI you can run the provided Streamlit app. This directly
uses the `ChatEngine` so no separate API server is required:

```bash
streamlit run frontend/chat_ui.py
```

Type your question in the input box and the assistant's answer will appear
below. Each interaction is shown so you can review the conversation history.
---

## 🧪 Testing

You can manually test:
```bash
python -c "from language_model.language_model import generate_answer; print(generate_answer([...]))"
```

Or run `main.py` and ask natural questions.

---

## 🔄 Extensibility

- Swap vector store in `vector_store/base.py` with FAISS/Pinecone.
- Switch from GROQ to OpenAI or Claude by modifying `language_model.py`.
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
