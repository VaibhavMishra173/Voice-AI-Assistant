from collections import deque
from typing import List, Tuple
from core.config import Config

class SessionMemory:
    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self.history = deque(maxlen=max_turns)  # stores tuples (question, answer)

    def add_turn(self, question: str, answer: str):
        self.history.append((question, answer))

    def get_history(self) -> List[Tuple[str, str]]:
        return list(self.history)

    def clear(self):
        self.history.clear()

    def get_formatted_context(self) -> str:
        if not self.history:
            return ""
        context = ""
        for i, (q, a) in enumerate(self.history, 1):
            context += f"Turn {i}:\nQ: {q}\nA: {a}\n\n"
        return context.strip()
