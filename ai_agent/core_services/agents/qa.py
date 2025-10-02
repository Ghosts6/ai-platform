import openai
import os
from .base import AgentBase
from core_services.models import AgentMemory
from typing import Dict, Any, List, Optional
from asgiref.sync import sync_to_async

openai.api_key = os.getenv("OPENAI_API_KEY")

class QAPairAgent(AgentBase):
    """
    An agent that stores prompt-answer pairs, can answer, list, update, and delete QAs.
    Uses OpenAI GPT for answers and stores them for future retrieval.
    """
    def __init__(self, agent_id: str, name: str, description: str = "", client=None):
        super().__init__(agent_id, name, description)
        self.client = client or openai.chat.completions

    @sync_to_async
    def _update_or_create_memory(self, key, value):
        AgentMemory.objects.update_or_create(agent_name=self.name, key=key, defaults={"value": value})

    @sync_to_async
    def _get_memory(self, key):
        return AgentMemory.objects.filter(agent_name=self.name, key=key).first()

    @sync_to_async
    def _delete_memory(self, key):
        return AgentMemory.objects.filter(agent_name=self.name, key=key).delete()

    @sync_to_async
    def _save_memory(self, mem):
        mem.save()

    async def process(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = task.get("prompt")
        if not prompt:
            raise ValueError("Prompt is missing from the task.")

        prompt_lower = prompt.lower()

        

        # Add QA: 'ask What is AI? Answer: Artificial Intelligence.'
        if prompt_lower.startswith("ask ") and "answer:" in prompt_lower:
            try:
                q, a = prompt.split("answer:", 1)
                q = q.replace("ask", "", 1).strip()
                a = a.strip()
                await self._update_or_create_memory(q, a)
                return {"result": f"Stored QA: '{q}' -> '{a}'"}
            except Exception:
                return {"error": "Invalid format. Use: ask <question> Answer: <answer>"}
        # Update QA: 'update <question> to <new answer>'
        elif prompt_lower.startswith("update ") and " to " in prompt_lower:
            try:
                _, rest = prompt.split("update", 1)
                q, a = rest.split("to", 1)
                q, a = q.strip(), a.strip()
                mem = await self._get_memory(q)
                if mem:
                    mem.value = a
                    await self._save_memory(mem)
                    return {"result": f"Updated answer for '{q}' to '{a}'"}
                return {"result": f"No QA found for '{q}'"}
            except Exception:
                return {"error": "Invalid update format. Use: update <question> to <new answer>"}
        # Delete QA: 'delete <question>'
        elif prompt_lower.startswith("delete "):
            q = prompt[7:].strip()
            deleted, _ = await self._delete_memory(q)
            if deleted:
                return {"result": f"Deleted QA for '{q}'"}
            return {"result": f"No QA found for '{q}'"}
        # Get answer from memory or OpenAI
        else:
            q = prompt.strip()
            mem = await self._get_memory(q)
            if mem:
                return {"result": f"Answer: {mem.value}"}

            # RAG workflow
            context_from_db = self.search_knowledge_base(q)

            if context_from_db:
                context_str = "\n\n".join(context_from_db)
                system_prompt = (
                    "You are a helpful assistant. Answer the user's question based on the following context. "
                    "If the context does not contain the answer, say that you don't know.\n\n"
                    f"Context:\n{context_str}"
                )
            else:
                system_prompt = "You are a helpful assistant."

            # If not found, ask OpenAI and store
            try:
                response = self.client.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": q}
                    ],
                    temperature=0.5,
                )
                msg = response.choices[0].message
                if isinstance(msg, dict):
                    answer = msg.get('content')
                else:
                    answer = msg.content
                await self._update_or_create_memory(q, answer)
                return {"result": f"Answer: {answer}"}
            except Exception as e:
                return {"error": f"Error: unable to get answer from OpenAI. {str(e)}"}

    def get_capabilities(self) -> List[str]:
        return ["ask_question", "add_qa", "update_qa", "delete_qa", "kiarash_bashokian_info"]
