"""
Manages the short-term conversation history.
"""

class SessionMemory:
    def __init__(self):
        self.history = [] # List of {"role": "user/assistant", "content": "..."}

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

    def get_history_string(self):
        """Returns history formatted for LLM context."""
        return "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in self.history])

    def clear(self):
        self.history = []
