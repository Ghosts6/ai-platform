from .base import AgentBase
from typing import Dict, Any, List, Optional
import openai
import os
import json
from ai_agent.core_services.models import Agent

class SummarizerAgent(AgentBase):
    def __init__(self, agent_instance: Agent, client=None, **kwargs):
        super().__init__(agent_instance)
        self.client = client or openai.OpenAI()

    async def process(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = task.get("prompt")
        if not prompt:
            raise ValueError("Prompt is missing from the task.")

        summary_length = task.get("summary_length", "medium")

        try:
            system_prompt = "You are a helpful summarizer."
            if summary_length in ["short", "medium", "long"]:
                system_prompt += f" Provide a {summary_length} summary."
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
            )
            choice = response.choices[0]
            summary = choice.message.content if hasattr(choice.message, 'content') else choice.message['content']
            
            await self.store_memory("last_summary", summary)
                
            return {"result": f"Summary: {summary}"}
        except Exception as e:
            return {"error": f"Error: unable to summarize the text. {str(e)}"}

    def get_capabilities(self) -> List[str]:
        return ["summarize_text"]