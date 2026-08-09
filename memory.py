from dataclasses import dataclass


@dataclass
class Message:
    role: str      # "user" or "assistant"
    content: str


class ConversationMemory:
    """session_id ごとに会話履歴をインメモリで保持する。

    ポートフォリオ用途なのでプロセス内の辞書で十分。
    本番では Redis などに差し替える前提。
    """

    def __init__(self, max_turns: int = 6):
        self.max_turns = max_turns              # 直近 N 往復だけ保持（トークン節約）
        self._store: dict[str, list[Message]] = {}

    def add(self, session_id: str, role: str, content: str) -> None:
        history = self._store.setdefault(session_id, [])
        history.append(Message(role=role, content=content))

        # 1往復 = user + assistant の2件なので max_turns * 2 で切る
        limit = self.max_turns * 2
        if len(history) > limit:
            del history[:-limit]

    def get(self, session_id: str) -> list[Message]:
        return list(self._store.get(session_id, []))

    def to_openai_messages(self, session_id: str) -> list[dict]:
        return [
            {"role": m.role, "content": m.content}
            for m in self._store.get(session_id, [])
        ]

    def clear(self, session_id: str) -> None:
        self._store.pop(session_id, None)

    def stats(self, session_id: str) -> dict:
        history = self._store.get(session_id, [])
        return {
            "turns": len(history) // 2,   # UIに会話ターン数を表示するため
            "total_chars": sum(len(m.content) for m in history),
        }


memory = ConversationMemory()  # シングルトン
