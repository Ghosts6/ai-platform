from .base import AgentBase
from typing import Dict, Any, List, Optional
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class EmailAgent(AgentBase):
    def __init__(self, agent_id: str, name: str, description: str = "", client=None):
        super().__init__(agent_id, name, description)
        self.client = client or openai.chat.completions

    async def process(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = task.get("prompt")
        if not prompt:
            raise ValueError("Prompt is missing from the task.")

        try:
            # Tool: Suggest reply, draft, or summarize email
            if any(word in prompt.lower() for word in ["suggest reply", "draft reply", "auto reply"]):
                system_prompt = "You are an AI email assistant. Suggest a professional reply to the following email."
            elif any(word in prompt.lower() for word in ["summarize", "analyze", "extract"]):
                system_prompt = "You are an AI email assistant. Summarize or analyze the following email."
            elif any(word in prompt.lower() for word in ["create new email", "compose email", "draft email"]):
                system_prompt = "You are an AI email assistant. Compose a new email based on the user's instructions."
            else:
                system_prompt = "You are an AI email assistant. Help with any email-related task."
            
            response = self.client.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
            )
            choice = response.choices[0]
            answer = choice.message.content if hasattr(choice.message, 'content') else choice.message['content']
            return {"result": f"EmailAgent: {answer}"}
        except Exception as e:
            return {"error": f"Error: unable to process email task. {str(e)}"}

    def get_capabilities(self) -> List[str]:
        return ["suggest_reply", "summarize_email", "draft_email"]

