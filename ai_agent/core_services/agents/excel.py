from .base import AgentBase
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class ExcelAgent(AgentBase):
    def __init__(self, name: str, client=None):
        super().__init__(name)
        self.client = client or openai.chat.completions

    def handle(self, prompt: str) -> str:
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
            if hasattr(choice, "message"):
                answer = choice.message['content']
            else:
                answer = choice['message']['content']
            return f"ExcelAgent: {answer}"
        except Exception as e:
            return f"Error: unable to process spreadsheet task. {str(e)}"

__all__ = ["ExcelAgent"]
