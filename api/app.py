import os
from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from chat_engine.chat_engine import ChatEngine
from chat_engine.modules.prompt_assembler import default_prompt_assembler
from chat_engine.modules.retriever import default_retriever
from embedding.embedder import embed_text
from language_model.language_model import generate_answer

security = HTTPBearer()

API_TOKEN = os.getenv("API_TOKEN", "secret-token")

engine = ChatEngine(
    retriever=default_retriever,
    embedder=embed_text,
    llm=generate_answer,
    prompt_assembler=default_prompt_assembler,
)

app = FastAPI(title="RAG_HEITAA API", version="1.0")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


def authenticate(creds: HTTPAuthorizationCredentials = Depends(security)):
    if creds.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")


class ChatRequest(BaseModel):
    question: str


@app.post("/v1/chat", dependencies=[Depends(authenticate)])
async def chat_endpoint(req: ChatRequest):
    answer = engine.answer_query(req.question)
    return {"answer": answer}


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
