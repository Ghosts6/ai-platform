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

---

# ────────────────
# AI Agents Overview & Setup
# ────────────────

## Available Agents

- **SummarizerAgent**: Summarizes text using OpenAI. No extra setup needed.
- **QAPairAgent**: Answers questions and stores Q&A pairs using OpenAI. No extra setup needed.
- **EmailAgent**: Summarizes, drafts, and analyzes emails using OpenAI. No extra setup needed.
- **ExcelAgent**: Suggests formulas, summarizes, and analyzes spreadsheet data using OpenAI. No extra setup needed.
- **TeamsAgent**: Connects to Microsoft Teams/Outlook, listens for events (e.g., maintenance, survey, test running), and creates calendar events automatically. Requires Microsoft Azure app registration and O365 setup (see below).

## How to Set Up Each Agent

### 1. SummarizerAgent, QAPairAgent, EmailAgent, ExcelAgent
- **Requirement:** OpenAI API key in `.env` as `OPENAI_API_KEY`.
- **Usage:** Accessible via `/api/agent/respond/` endpoint. Just send a prompt.

### 2. TeamsAgent (Microsoft Teams/Calendar Integration)
- **Requirements:**
  - Register an app in Azure Portal (Azure Active Directory > App registrations).
  - Add the following to your `.env`:
    - `MS_CLIENT_ID`
    - `MS_CLIENT_SECRET`
    - `MS_TENANT_ID`
    - `MS_REDIRECT_URI` (e.g., `http://localhost:8000/msauth/callback/`)
  - Install Python package: `pip install O365`
- **First Run:**
  - On first use, you will be prompted to authenticate in a browser. This will save a token file for future use.
- **Usage:**
  - Send a prompt containing keywords like "maintenance", "survey", or "test running" to `/api/agent/respond/`.
  - The agent will create a calendar event in your default Teams/Outlook calendar.

## Example .env File

```env
# Django & Database
DJANGO_SECRET_KEY=your-django-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=your_db
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# OpenAI
OPENAI_API_KEY=your-openai-key

# Celery/Redis
CELERY_BROKER_URL=redis://localhost:6379/0

# Microsoft Teams/Graph API
MS_CLIENT_ID=your-client-id
MS_CLIENT_SECRET=your-client-secret
MS_TENANT_ID=your-tenant-id
MS_REDIRECT_URI=http://localhost:8000/msauth/callback/

# Test Mode
TEST_MODE=True
```

