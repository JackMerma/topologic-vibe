from dataclasses import dataclass


class TopologicSession:
    def __init__(self):
        self.items = {}
        self.messages = []

    def add(self, name, obj):
        self.items[name] = obj
        return f"Object '{name}' saved."

    def get_all_names(self):
        return list(self.items.keys())

    def get(self, name):
        return self.items.get(name, None)

    def add_message(self, role: str, content: str):
        entry = {"role": role, "content": content}
        self.messages.append(entry)
        return entry

    def get_messages(self):
        return list(self.messages)

    def clear_messages(self):
        self.messages = []
        return True


@dataclass
class SessionContext:
    session: TopologicSession