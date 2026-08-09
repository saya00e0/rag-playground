import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from openai import OpenAIError
from pydantic import BaseModel

from chat_chain import chat
from memory import memory
from retriever import retrieve, answer

app = FastAPI(title="Simple RAG Demo")
templates = Jinja2Templates(directory="templates")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 4

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/query")
async def query_endpoint(req: QueryRequest):
    chunks = retrieve(req.query, top_k=req.top_k)
    response = answer(req.query, chunks)
    return {
        "answer": response,
        "sources": [
            {
                "text": c.text[:200] + "...",
                "source": c.source,
                "score": round(c.score, 3),  # ← UIで類似度スコアを見せる
            }
            for c in chunks
        ],
    }

# --- Week 2: チャット履歴付きRAG ---

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat/new")
async def chat_new():
    return {"session_id": str(uuid.uuid4())}

@app.post("/chat/message")
async def chat_message(req: ChatRequest):
    if not req.session_id.strip():
        raise HTTPException(status_code=400, detail="session_id is required")
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="message is required")

    try:
        return chat(req.session_id, req.message)
    except OpenAIError:
        # 詳細（スタックトレース・APIキー等）はレスポンスに含めない
        raise HTTPException(status_code=503, detail="LLM service unavailable")

@app.delete("/chat/{session_id}")
async def chat_reset(session_id: str):
    memory.clear(session_id)
    return {"status": "cleared", "session_id": session_id}
