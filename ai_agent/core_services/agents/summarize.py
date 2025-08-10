from .base import AgentBase
from typing import Dict, Any, List, Optional
import openai
import os
from asgiref.sync import sync_to_async

openai.api_key = os.getenv("OPENAI_API_KEY")

class SummarizerAgent(AgentBase):
    def __init__(self, agent_id: str, name: str, description: str = "", client=None, memory_backend=None):
        super().__init__(agent_id, name, description)
        self.client = client or openai.chat.completions
        self.memory_backend = memory_backend

    async def process(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = task.get("prompt")
        if not prompt:
            raise ValueError("Prompt is missing from the task.")

        summary_length = task.get("summary_length", "medium")

        try:
            system_prompt = "You are a helpful summarizer."
            if summary_length in ["short", "medium", "long"]:
                system_prompt += f" Provide a {summary_length} summary."
            
            response = self.client.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
            )
            choice = response.choices[0]
            summary = choice.message.content if hasattr(choice.message, 'content') else choice.message['content']
            
            if self.memory_backend:
                await sync_to_async(self.memory_backend)(self.name, "last_summary", summary)
                
            return {"result": f"Summary: {summary}"}
        except Exception as e:
            return {"error": f"Error: unable to summarize the text. {str(e)}"}

    def get_capabilities(self) -> List[str]:
        return ["summarize_text"]