import openai
import os
from .base import AgentBase
from core_services.models import AgentMemory

openai.api_key = os.getenv("OPENAI_API_KEY")

class QAPairAgent(AgentBase):
    """
    An agent that stores prompt-answer pairs, can answer, list, update, and delete QAs.
    Uses OpenAI GPT for answers and stores them for future retrieval.
    """
    def __init__(self, name: str, client=None):
        super().__init__(name)
        self.client = client or openai.chat.completions

    def handle(self, prompt: str) -> str:
        import json
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
                return f"Kiarash Bashokian's skills: {skills}"
            elif any(k in prompt_lower for k in ["experience", "work", "background"]):
                return f"Kiarash Bashokian's experience: {experience}"
            elif any(k in prompt_lower for k in ["education", "study", "degree"]):
                return f"Kiarash Bashokian's education: {education}"
            elif any(k in prompt_lower for k in ["language", "languages"]):
                return f"Languages: {languages}"
            elif any(k in prompt_lower for k in ["contact", "email", "phone"]):
                return "Contact: kiarash@kiarashbashokian.com | +1 416-732-8976 | Toronto, ON M3J 1P3."
            elif any(k in prompt_lower for k in ["website", "profile", "portfolio", "linkedin", "github"]):
                return "Websites & Profiles: https://www.linkedin.com/in/kiarashbashokian/ | http://www.kiarashbashokian.com | https://github.com/Ghosts6"
            else:
                return bio

        # Add QA: 'ask What is AI? Answer: Artificial Intelligence.'
        if prompt_lower.startswith("ask ") and "answer:" in prompt_lower:
            try:
                q, a = prompt.split("answer:", 1)
                q = q.replace("ask", "", 1).strip()
                a = a.strip()
                AgentMemory.objects.update_or_create(
                    agent_name=self.name, key=q, defaults={"value": a}
                )
                return f"Stored QA: '{q}' -> '{a}'"
            except Exception:
                return "Invalid format. Use: ask <question> Answer: <answer>"
        # Update QA: 'update <question> to <new answer>'
        elif prompt_lower.startswith("update ") and " to " in prompt_lower:
            try:
                _, rest = prompt.split("update", 1)
                q, a = rest.split("to", 1)
                q, a = q.strip(), a.strip()
                mem = AgentMemory.objects.filter(agent_name=self.name, key=q).first()
                if mem:
                    mem.value = a
                    mem.save()
                    return f"Updated answer for '{q}' to '{a}'"
                return f"No QA found for '{q}'"
            except Exception:
                return "Invalid update format. Use: update <question> to <new answer>"
        # Delete QA: 'delete <question>'
        elif prompt_lower.startswith("delete "):
            q = prompt[7:].strip()
            deleted, _ = AgentMemory.objects.filter(agent_name=self.name, key=q).delete()
            if deleted:
                return f"Deleted QA for '{q}'"
            return f"No QA found for '{q}'"
        # Get answer from memory or OpenAI
        else:
            q = prompt.strip().lower().rstrip('?')
            mem = AgentMemory.objects.filter(agent_name=self.name, key=q).first()
            if mem:
                return f"Answer: {mem.value}"
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
                AgentMemory.objects.update_or_create(
                    agent_name=self.name, key=q, defaults={"value": answer}
                )
                return f"Answer: {answer}"
            except Exception as e:
                return f"Error: unable to get answer from OpenAI. {str(e)}"