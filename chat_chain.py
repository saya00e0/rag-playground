from openai import OpenAI
from dotenv import load_dotenv

from memory import memory
from retriever import retrieve, RetrievedChunk

load_dotenv()
client = OpenAI()

CONDENSE_PROMPT = """以下の会話履歴と続く質問を踏まえて、質問を単体で意味が通る検索クエリに言い換えてください。
「それ」「その」などの代名詞は履歴を参照して具体的な語に置き換えてください。
言い換えた質問だけを出力し、説明や前置きは付けないでください。
言い換える必要がなければ、元の質問をそのまま出力してください。"""

SYSTEM_PROMPT = """あなたは社内ドキュメントに基づいて回答するアシスタントです。
以下のコンテキストのみを使って質問に答えてください。
コンテキストに情報がない場合は「資料に記載がありません」と答えてください。
会話履歴は文脈の理解にだけ使い、履歴から事実を推測しないでください。

コンテキスト:
{context}"""


def condense_question(session_id: str, question: str) -> str:
    """会話履歴を踏まえて、単体で意味が通る検索クエリに言い換える。"""
    history = memory.to_openai_messages(session_id)
    if not history:
        return question   # 初回は言い換え不要（余計な API コールを防ぐ）

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": CONDENSE_PROMPT},
            *history,
            {"role": "user", "content": f"続く質問: {question}"},
        ],
        temperature=0,   # 言い換えは再現性重視
    )
    return res.choices[0].message.content.strip()


def chat(session_id: str, user_question: str) -> dict:
    # Step 1: 履歴を踏まえて質問を言い換える
    condensed = condense_question(session_id, user_question)

    # Step 2: 言い換えた質問でベクトル検索
    chunks = retrieve(condensed)
    context = "\n\n---\n\n".join(
        f"[出典: {c.source}]\n{c.text}" for c in chunks
    )

    # system プロンプトは会話履歴より前に置く（後ろだと効きが薄い）
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
        *memory.to_openai_messages(session_id),
        {"role": "user", "content": user_question},
    ]
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0,
    )
    answer = res.choices[0].message.content

    # 履歴に積むのは言い換え前のユーザー発話（会話の記録なので原文を残す）
    memory.add(session_id, "user", user_question)
    memory.add(session_id, "assistant", answer)

    return {
        "answer": answer,
        "condensed_question": condensed,
        "sources": [_to_source(c) for c in chunks],
        "memory_stats": memory.stats(session_id),
    }


def _to_source(chunk: RetrievedChunk) -> dict:
    text = chunk.text[:200]
    if len(chunk.text) > 200:
        text += "..."
    return {
        "text": text,
        "source": chunk.source,
        "score": round(chunk.score, 3),
    }
