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

        # --- Custom info about Kiarash Bashokian ---
        bio = (
            "Kiarash Bashokian is a Backend Developer based in Toronto, ON, specializing in scalable and secure web solutions. "
            "He has a strong IT infrastructure background and is proficient in building high-performance systems using Monolithic and Hybrid Architectures. "
            "Kiarash is skilled in Python, JavaScript, C++, and frameworks such as Django, FastAPI, and Flask for secure and efficient web applications. "
            "He is experienced in MPA + SSR and SPA + SSR architectures, SQL/NoSQL databases (PostgreSQL, MySQL, MongoDB, Redis), and CI/CD pipelines. "
            "He has a solid foundation in Linux Systems Administration and Network Infrastructure Management, optimizing deployment and security. "
            "Passionate about problem-solving, performance optimization, and continuous learning to drive innovation in backend development. "
            "Contact: kiarash@kiarashbashokian.com | +1 416-732-8976 | Toronto, ON M3J 1P3. "
            "Websites & Profiles: https://www.linkedin.com/in/kiarashbashokian/ | http://www.kiarashbashokian.com | https://github.com/Ghosts6"
        )
        skills = (
            "Python, JavaScript, C/C++, Django, Django REST Framework (DRF), FastAPI, Flask, PostgreSQL, MySQL, MongoDB, Redis, HTML/CSS, Tailwind CSS, React, pytest, Git/Docker, "
            "Linux Systems Administration (Arch, Ubuntu, Debian), Network Infrastructure Management."
        )
        experience = (
            "Web Developer at Gh Light (Tehran, Iran, 03/2024 - 05/2024): Developed website backend, frontend, SEO, and database; optimized systems. "
            "IT Expert at Arya Heavy Machinery (Tehran, Iran, 11/2023 - 02/2024): Managed HP servers, vCenter, firewalls, Cisco devices, SAP system support, network management. "
            "Trainee Qt Developer (Tehran, Iran, 09/2022 - 12/2022): Enhanced C++/C OOP and memory management, worked with Qt framework. "
        )
        education = "Bachelor of Computer Science: Software, York University, Toronto, Ontario, Canada, expected 02/2025."
        languages = "English: Professional, Persian: Professional."

        # --- Expanded matching for questions about Kiarash Bashokian ---
        def is_about_kiarash(text):
            keywords = [
                "kiarash", "bashokian", "about kiarash", "who is kiarash", "kiarash's background",
                "kiarash bashokian", "kiarash's skills", "kiarash's experience", "kiarash's education",
                "tell me about kiarash", "what does kiarash do", "linkedin kiarash", "github kiarash",
                "kiarash cv", "kiarash resume", "kiarash profile", "kiarash website", "kiarash contact"
            ]
            return any(k in text for k in keywords)

        if is_about_kiarash(prompt_lower):
            # Skill/experience/education/language/contact detection
            if any(k in prompt_lower for k in ["skill", "skills"]):
                return {"result": f"Kiarash Bashokian's skills: {skills}"}
            elif any(k in prompt_lower for k in ["experience", "work", "background"]):
                return {"result": f"Kiarash Bashokian's experience: {experience}"}
            elif any(k in prompt_lower for k in ["education", "study", "degree"]):
                return {"result": f"Kiarash Bashokian's education: {education}"}
            elif any(k in prompt_lower for k in ["language", "languages"]):
                return {"result": f"Languages: {languages}"}
            elif any(k in prompt_lower for k in ["contact", "email", "phone"]):
                return {"result": "Contact: kiarash@kiarashbashokian.com | +1 416-732-8976 | Toronto, ON M3J 1P3."}
            elif any(k in prompt_lower for k in ["website", "profile", "portfolio", "linkedin", "github"]):
                return {"result": "Websites & Profiles: https://www.linkedin.com/in/kiarashbashokian/ | http://www.kiarashbashokian.com | https://github.com/Ghosts6"}
            else:
                return {"result": bio}

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
            # If not found, ask OpenAI and store
            try:
                # Add full CV and links to system prompt for context
                system_prompt = (
                    "You are a helpful assistant. If the user asks about Kiarash Bashokian, answer with this info: "
                    f"{bio}\nSkills: {skills}\nExperience: {experience}\nEducation: {education}\nLanguages: {languages}\nWebsites & Profiles: https://www.linkedin.com/in/kiarashbashokian/ | http://www.kiarashbashokian.com | https://github.com/Ghosts6\nContact: kiarash@kiarashbashokian.com | +1 416-732-8976 | Toronto, ON M3J 1P3."
                )
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
