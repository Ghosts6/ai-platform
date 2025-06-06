from .base import AgentBase

class ExcelAgent(AgentBase):
    def handle(self, prompt: str) -> str:
        # Simple logic: recognize spreadsheet tasks
        if 'summarize' in prompt.lower():
            return "Excel Summary: This is a summary of your spreadsheet."
        elif 'analyze' in prompt.lower():
            return "Excel Analysis: The data shows positive growth."
        elif 'read' in prompt.lower():
            return "Excel Read: Sheet1 contains 10 rows."
        return "ExcelAgent: No actionable spreadsheet task detected."

__all__ = ["ExcelAgent"]
