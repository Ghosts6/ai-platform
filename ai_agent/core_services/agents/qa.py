import openai
import os
import re
from .base import AgentBase
from typing import Dict, Any, List, Optional
import json

class QAPairAgent(AgentBase):
    """
    An agent that stores prompt-answer pairs, can answer, list, update, and delete QAs.
    Uses OpenAI GPT for answers and stores them for future retrieval.
    """
    def __init__(self, agent_instance, client=None, **kwargs):
        super().__init__(agent_instance)
        self.client = client or openai.OpenAI()
        self.commands = {
            "add_qa": re.compile(r"ask\s+(?P<question>.+?)\s+answer:\s*(?P<answer>.+)", re.IGNORECASE),
            "update_qa": re.compile(r"update\s+(?P<question>.+?)\s+to\s+(?P<answer>.+)", re.IGNORECASE),
            "delete_qa": re.compile(r"delete\s+(?P<question>.+)", re.IGNORECASE),
            "list_qas": re.compile(r"list qas", re.IGNORECASE),
        }

    async def _handle_add_qa(self, question: str, answer: str) -> Dict[str, Any]:
        await self.store_memory(question, {"answer": answer})
        return {"result": f"Stored QA: '{question}' -> '{answer}'"}

    async def _handle_update_qa(self, question: str, answer: str) -> Dict[str, Any]:
        existing_qa = await self.retrieve_memory(question)
        if existing_qa:
            await self.store_memory(question, {"answer": answer})
            return {"result": f"Updated answer for '{question}' to '{answer}'"}
        return {"result": f"No QA found for '{question}' to update."}

    async def _handle_delete_qa(self, question: str) -> Dict[str, Any]:
        await self.store_memory(question, None) # Overwrite with None to signify deletion
        return {"result": f"Deleted QA for '{question}'"}

    async def _handle_list_qas(self) -> Dict[str, Any]:
        if not self.memory:
            await self._load_memory()
        
        qa_list = [f"Q: {q}, A: {data['value']['answer']}" for q, data in self.memory.items() if data and 'answer' in data.get('value', {})]
        
        if qa_list:
            return {"result": "Stored QAs:\n" + "\n".join(qa_list)}
        return {"result": "No QAs found."}

    async def _handle_question(self, question: str) -> Dict[str, Any]:
        memory_data = await self.retrieve_memory(question)
        if memory_data and memory_data.get("answer"):
            return {"result": f"Answer: {memory_data['answer']}"}

        # RAG workflow
        context_from_db = await self.search_knowledge_base(question)
        system_prompt = "You are a helpful assistant."
        if context_from_db:
            context_str = "\n\n".join(context_from_db)
            system_prompt = (
                "You are a helpful assistant. Answer the user's question based on the context. "
                "If the context does not contain the answer, say that you don't know.\n\n"
                f"Context:\n{context_str}"
            )
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": question}],
                temperature=0.5,
            )
            answer = response.choices[0].message.content
            # Only store in memory if it's a definitive answer, not a "I don't know" response
            if not re.search(r"i don't know|i cannot answer|not found", answer, re.IGNORECASE):
                await self.store_memory(question, {"answer": answer})
            return {"result": f"Answer: {answer}"}
        except Exception as e:
            return {"error": f"Error: unable to get answer from OpenAI. {str(e)}"}

    async def process(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = task.get("prompt", "").strip()
        if not prompt:
            raise ValueError("Prompt is missing from the task.")

        for command_name, pattern in self.commands.items():
            match = pattern.match(prompt)
            if match:
                data = match.groupdict()
                if command_name == "add_qa":
                    return await self._handle_add_qa(data['question'], data['answer'])
                elif command_name == "update_qa":
                    return await self._handle_update_qa(data['question'], data['answer'])
                elif command_name == "delete_qa":
                    return await self._handle_delete_qa(data['question'])
                elif command_name == "list_qas":
                    return await self._handle_list_qas()
        
        return await self._handle_question(prompt)

    def get_capabilities(self) -> List[str]:
        return ["ask_question", "add_qa", "update_qa", "delete_qa", "list_qas"]