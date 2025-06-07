# DEPRECATED: This file is no longer used. ListAgent has been removed in favor of AI-powered agents only.
# This file will be deleted in a future cleanup.

import json
from .base import AgentBase
from core_services.models import AgentMemory

class ListAgent(AgentBase):
    """
    An agent that manages a persistent list (add, remove, list, clear, update items) in its memory.
    """
    def __init__(self, name: str):
        super().__init__(name)

    def _get_list(self):
        mem = AgentMemory.objects.filter(agent_name=self.name, key="list").first()
        if mem:
            try:
                return json.loads(mem.value)
            except Exception:
                return []
        return []

    def _save_list(self, items):
        AgentMemory.objects.update_or_create(
            agent_name=self.name, key="list", defaults={"value": json.dumps(items)}
        )

    def handle(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        items = self._get_list()
        if "add" in prompt_lower:
            # Add item: 'add milk'
            item = prompt.split("add", 1)[-1].strip()
            if item:
                items.append(item)
                self._save_list(items)
                return f"Added '{item}' to the list."
            return "No item specified to add."
        elif "remove" in prompt_lower:
            # Remove item: 'remove milk'
            item = prompt.split("remove", 1)[-1].strip()
            if item in items:
                items.remove(item)
                self._save_list(items)
                return f"Removed '{item}' from the list."
            return f"Item '{item}' not found in the list."
        elif "clear" in prompt_lower:
            self._save_list([])
            return "List cleared."
        elif "list" in prompt_lower or "show" in prompt_lower:
            if items:
                return "Current list: " + ", ".join(items)
            return "List is empty."
        elif "update" in prompt_lower:
            # update milk to bread
            try:
                _, rest = prompt_lower.split("update", 1)
                old, new = rest.split("to")
                old, new = old.strip(), new.strip()
                if old in items:
                    idx = items.index(old)
                    items[idx] = new
                    self._save_list(items)
                    return f"Updated '{old}' to '{new}'."
                return f"Item '{old}' not found in the list."
            except Exception:
                return "Invalid update command. Use: update <old> to <new>"
        return "Unknown list command. Try: add, remove, update, clear, list."
