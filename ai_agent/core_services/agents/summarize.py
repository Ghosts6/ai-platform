from .base import AgentBase
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class SummarizerAgent(AgentBase):
    def __init__(self, name: str, client=None):
        super().__init__(name)
        # Use the new OpenAI API endpoint
        self.client = client or openai.chat.completions

    def handle(self, prompt: str, summary_length: str = "medium") -> str:
        """
        Handles summarization. Optionally accepts summary_length: 'short', 'medium', 'long'.
        """
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
            # Support both dict and object for test mocks
            choice = response.choices[0]
            if hasattr(choice, "message"):
                summary = choice.message['content']
            else:
                summary = choice['message']['content']
            return f"Summary: {summary}"
        except Exception as e:
            return f"Error: unable to summarize the text. {str(e)}"
