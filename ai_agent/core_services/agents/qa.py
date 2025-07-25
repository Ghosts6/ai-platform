import openai
import os
from .base import AgentBase
from core_services.models import AgentMemory

openai.api_key = os.getenv("OPENAI_API_KEY")

class QAPairAgent(AgentBase):
    """
    An agent that stores prompt-answer pairs, can answer, list, update, and delete QAs.
    Uses OpenAI GPT for answers and stores them for future retrieval.
    """
    def __init__(self, name: str, client=None):
        super().__init__(name)
        self.client = client or openai.chat.completions

    def handle(self, prompt: str) -> str:
        import json
        prompt_lower = prompt.lower()

        # Handle questions about Kiarash Bashokian
        if 'kiarash bashokian' in prompt_lower:
            if 'skill' in prompt_lower:
                mem = AgentMemory.objects.filter(agent_name=self.name, key="what are kiarash bashokian's skills").first()
                if mem:
                    return f"Answer: {mem.value}"
            elif 'experience' in prompt_lower or 'work' in prompt_lower:
                mem = AgentMemory.objects.filter(agent_name=self.name, key="what is kiarash bashokian's experience").first()
                if mem:
                    return f"Answer: {mem.value}"
            elif 'education' in prompt_lower or 'study' in prompt_lower:
                mem = AgentMemory.objects.filter(agent_name=self.name, key="where did kiarash bashokian study").first()
                if mem:
                    return f"Answer: {mem.value}"
            else:
                mem = AgentMemory.objects.filter(agent_name=self.name, key="who is kiarash bashokian").first()
                if mem:
                    return f"Answer: {mem.value}"

        # Add QA: 'ask What is AI? Answer: Artificial Intelligence.'
        if prompt_lower.startswith("ask ") and "answer:" in prompt_lower:
            try:
                q, a = prompt.split("answer:", 1)
                q = q.replace("ask", "", 1).strip()
                a = a.strip()
                AgentMemory.objects.update_or_create(
                    agent_name=self.name, key=q, defaults={"value": a}
                )
                return f"Stored QA: '{q}' -> '{a}'"
            except Exception:
                return "Invalid format. Use: ask <question> Answer: <answer>"
        # Update QA: 'update <question> to <new answer>'
        elif prompt_lower.startswith("update ") and " to " in prompt_lower:
            try:
                _, rest = prompt.split("update", 1)
                q, a = rest.split("to", 1)
                q, a = q.strip(), a.strip()
                mem = AgentMemory.objects.filter(agent_name=self.name, key=q).first()
                if mem:
                    mem.value = a
                    mem.save()
                    return f"Updated answer for '{q}' to '{a}'"
                return f"No QA found for '{q}'"
            except Exception:
                return "Invalid update format. Use: update <question> to <new answer>"
        # Delete QA: 'delete <question>'
        elif prompt_lower.startswith("delete "):
            q = prompt[7:].strip()
            deleted, _ = AgentMemory.objects.filter(agent_name=self.name, key=q).delete()
            if deleted:
                return f"Deleted QA for '{q}'"
            return f"No QA found for '{q}'"
        # Get answer from memory or OpenAI
        else:
            q = prompt.strip().lower().rstrip('?')
            mem = AgentMemory.objects.filter(agent_name=self.name, key=q).first()
            if mem:
                return f"Answer: {mem.value}"
            # If not found, ask OpenAI and store
            try:
                response = self.client.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": q}
                    ],
                    temperature=0.5,
                )
                msg = response.choices[0].message
                if isinstance(msg, dict):
                    answer = msg.get('content')
                else:
                    answer = msg.content
                AgentMemory.objects.update_or_create(
                    agent_name=self.name, key=q, defaults={"value": answer}
                )
                return f"Answer: {answer}"
            except Exception as e:
                return f"Error: unable to get answer from OpenAI. {str(e)}"