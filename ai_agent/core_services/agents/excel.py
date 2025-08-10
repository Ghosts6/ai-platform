from .base import AgentBase
from typing import Dict, Any, List, Optional
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class ExcelAgent(AgentBase):
    def __init__(self, agent_id: str, name: str, description: str = "", client=None):
        super().__init__(agent_id, name, description)
        self.client = client or openai.chat.completions

    async def process(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = task.get("prompt")
        if not prompt:
            raise ValueError("Prompt is missing from the task.")

        try:
            # Tool: Suggest formula, summarize, or extract data
            if any(word in prompt.lower() for word in ["suggest formula", "generate formula", "excel formula"]):
                system_prompt = "You are an AI spreadsheet assistant. Suggest an Excel formula for the user's request."
            elif any(word in prompt.lower() for word in ["summarize", "analyze", "extract", "table summary"]):
                system_prompt = "You are an AI spreadsheet assistant. Summarize or analyze the following spreadsheet data."
            elif any(word in prompt.lower() for word in ["create new sheet", "new spreadsheet", "generate table"]):
                system_prompt = "You are an AI spreadsheet assistant. Create a new spreadsheet or table based on the user's instructions."
            else:
                system_prompt = "You are an AI spreadsheet assistant. Help with any spreadsheet-related task."
            
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
            return {"result": f"ExcelAgent: {answer}"}
        except Exception as e:
            return {"error": f"Error: unable to process spreadsheet task. {str(e)}"}

    def get_capabilities(self) -> List[str]:
        return ["suggest_formula", "summarize_data", "create_sheet"]

__all__ = ["ExcelAgent"]

