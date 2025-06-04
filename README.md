# 🧠 AIAgent

![baner](https://github.com/Ghosts6/Local-website/blob/main/img/Baner.png)

AIAgent is a modular backend framework designed to build and manage intelligent, task-oriented agents powered by OpenAI and other AI tools. The system provides a robust foundation for automating workflows such as responding to emails, updating calendars, processing spreadsheets, and integrating with external services.

This is the **base version**, architected for extensibility. It’s intended to be forked or extended into domain-specific assistants — such as social media managers, file analyzers, or enterprise support bots — with minimal effort.

---

## 🎯 Project Goals

- Create a flexible and reusable backend architecture for AI agent development
- Integrate LLM capabilities (OpenAI) into workflow automation
- Enable time-based and reactive scheduling of tasks
- Provide a testable, CI-ready foundation for future custom features
- Support future frontend integration or API-only usage

---

## ⚙️ Technologies & Architecture

- **Language & Framework**: Python 3.11+, Django 4.x, Django REST Framework
- **AI & LLM**: OpenAI API (ChatGPT, GPT-4)
- **Database**: PostgreSQL (SQLite supported for development)
- **Background Tasks**: Celery with Redis broker, APScheduler for timed jobs
- **Testing**: pytest, pytest-django, GitHub Actions CI pipeline
- **Environment Management**: `.env` with `python-dotenv`, Docker (optional)
- **Static Handling**: WhiteNoise for static files in production
- **Code Structure**: Microservice-like Django apps with isolated concerns

---

## 🧱 Microservice Breakdown

```
ai_agent/
├── ai_agent/          → Core Django settings and routing
├── agent/             → Core LLM agent logic, prompt runners, tasks
├── core_services/     → Shared models, auth, config, and custom commands
├── scheduler/         → Celery tasks and scheduled logic (via APScheduler)
├── shared_utils/      → Common code (OpenAI client, loggers, parsers)
├── tests/             → Pytest-based testing suite
├── .env               → Environment configuration
├── .github/           → GitHub Actions CI
└── requirements.txt   → Project dependencies
```

---

## 🧠 Planned Features

- ✅ Modular, reusable app structure
- ✅ LLM integration with OpenAI for dynamic prompt handling
- ✅ REST APIs via DRF for external communication
- ✅ Support for email processing, scheduling, and document parsing
- ✅ Custom Django management commands for automation
- ✅ Pytest integration with reusable test structure
- ✅ CI pipeline (test on push and PR)
- 🔜 Plugin system for domain-specific agents (email agent, Excel reader, etc.)
- 🔜 Agent state tracking and observability
- 🔜 Admin panel with agent logs and manual triggers

---

## 🧪 Development Setup

1. Clone the repository and navigate into it.
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create your `.env` file based on `.env.example`.
5. Run initial migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## 🚀 Running Tests

Run all tests using `pytest`:
```bash
pytest
```

Tests will also be executed automatically via GitHub Actions on push and pull request events.

