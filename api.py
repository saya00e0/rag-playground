from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from retriever import retrieve, answer

app = FastAPI(title="Simple RAG Demo")
templates = Jinja2Templates(directory="templates")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 4

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
