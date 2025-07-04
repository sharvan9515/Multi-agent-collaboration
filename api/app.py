import os
from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel

from utilities.text_to_speech import text_to_speech_base64

from core.chat_engine.chat_engine import ChatEngine
from core.chat_engine.modules.prompt_assembler import default_prompt_assembler
from core.chat_engine.modules.retriever import default_retriever
from core.embedding.embedder import embed_text
from core.language_model.language_model import generate_answer
from core.vector_store.base import init_collection

security = HTTPBearer()

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise RuntimeError("API_TOKEN environment variable must be set")

engine = ChatEngine(
    retriever=default_retriever,
    embedder=embed_text,
    llm=generate_answer,
    prompt_assembler=default_prompt_assembler,
)

app = FastAPI(title="RAG_HEITAA API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup() -> None:
    """Ensure the Qdrant collection exists before handling requests."""
    init_collection()


def authenticate(creds: HTTPAuthorizationCredentials = Depends(security)):
    if creds.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")


class ChatRequest(BaseModel):
    question: str


@app.post("/v1/chat", dependencies=[Depends(authenticate)])
async def chat_endpoint(req: ChatRequest):
    """Answer the user's question and return audio in a thread pool."""
    answer = await run_in_threadpool(engine.answer_query, req.question)
    audio = await run_in_threadpool(text_to_speech_base64, answer)
    return {"answer": answer, "audio": audio}


# GraphQL setup using strawberry
import strawberry
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Query:
    @strawberry.field
    def chat(self, info, question: str) -> str:
        return engine.answer_query(question)

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/v1/graphql", dependencies=[Depends(authenticate)])

# Serve the frontend after API routes to avoid route conflicts
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
