from .base import AgentBase
# EmailAgent: Uses OpenAI to summarize or analyze email content based on prompt
import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

class EmailAgent(AgentBase):
    def __init__(self, name: str, client=None):
        super().__init__(name)
        self.client = client or openai.chat.completions

    def handle(self, prompt: str) -> str:
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
            if hasattr(choice, "message"):
                answer = choice.message['content']
            else:
                answer = choice['message']['content']
            return f"EmailAgent: {answer}"
        except Exception as e:
            return f"Error: unable to process email task. {str(e)}"
