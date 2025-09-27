# 🧠 AIAgent

![baner](/img/Baner.png)

AIAgent is a full-stack framework for building and managing intelligent, task-oriented agents. It combines a powerful Django backend with a modern React frontend, providing a robust foundation for automating workflows and interacting with AI models.

This project is designed for extensibility, allowing you to create domain-specific assistants—such as social media managers, file analyzers, or enterprise support bots—with a complete user interface.

---

## 🎯 Project Goals

- **Full-Stack AI Platform**: Provide a seamless integration of a Django backend and React frontend.
- **Flexible Backend Architecture**: Create a reusable and scalable backend for AI agent development.
- **Interactive Web UI**: Offer a user-friendly interface for interacting with agents and viewing results.
- **LLM Integration**: Integrate Large Language Model (LLM) capabilities from OpenAI into automated workflows.
- **Extensible Agent System**: Support a variety of agents for tasks like email, calendar, and data analysis.
- **Testable and CI-Ready**: Ensure a solid foundation for future development with a comprehensive test suite.

---

## ⚙️ Technologies & Architecture

- **Backend**: Python 3.11+, Django 4.x, Django REST Framework
- **Frontend**: React, React Router, Axios, Tailwind CSS
- **AI & LLM**: OpenAI API (ChatGPT, GPT-4)
- **Containerization**: Docker, Docker Compose
- **Database**: PostgreSQL (SQLite supported for development)
- **Background Tasks**: Celery with Redis broker, APScheduler for timed jobs
- **Testing**: pytest, pytest-django, GitHub Actions CI pipeline
- **Environment Management**: `.env` with `python-dotenv`
- **Static Handling**: WhiteNoise for serving static files in production

---

## 🧱 Project Structure

```
.
├── ai_agent/          → Django backend project
│   ├── agent/         → Core LLM agent logic and tasks
│   ├── core_services/ → Shared models, services, and agent definitions
│   ├── scheduler/     → Celery tasks and scheduled jobs
│   ├── requirements.txt → Python dependencies
│   └── ...
├── frontend/          → React frontend application
│   ├── src/           → Source code for the React app
│   │   ├── components/  → Reusable UI components
│   │   ├── pages/       → Application pages
│   │   └── api/         → API integration (Axios)
│   └── public/        → Static assets and index.html
├── docker-compose.yml → Docker service definitions
└── package.json       → Frontend dependencies
```

---

## 🧠 Features

- ✅ **Modular Backend**: Reusable Django apps for core services, agents, and scheduling.
- ✅ **React Frontend**: A dynamic and responsive user interface for interacting with the AI agents.
- ✅ **LLM Integration**: Seamlessly connect with OpenAI for dynamic prompt handling.
- ✅ **REST APIs**: Communicate between the frontend and backend using Django REST Framework.
- ✅ **Pre-built Agents**: Includes agents for summarization, Q&A, email, Excel, and Teams calendar integration.
- ✅ **Custom Commands**: Automate tasks with custom Django management commands.
- ✅ **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions.

---

## 🧪 Development Setup

### Backend

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/AIAgent.git
    cd AIAgent
    ```
2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  **Install Python dependencies**:
    ```bash
    pip install -r ai_agent/requirements.txt
    ```
4.  **Set up your environment variables**:
    - Create a `.env` file in the `ai_agent` directory.
    - Use the provided `Example .env File` section as a template.
5.  **Run database migrations**:
    ```bash
    python ai_agent/manage.py migrate
    ```
6.  **Start the Django development server**:
    ```bash
    python ai_agent/manage.py runserver
    ```

### Frontend

1.  **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```
2.  **Install Node.js dependencies**:
    ```bash
    npm install
    ```
3.  **Start the React development server**:
    ```bash
    npm start
    ```
    The frontend will be available at `http://localhost:3000` and will proxy API requests to the Django backend.

---

## 🐳 Running with Docker

This project is fully containerized using Docker and Docker Compose, providing a consistent and reproducible environment.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### First-Time Setup

1.  **Environment Variables**: Ensure you have a valid `.env` file inside the `ai_agent` directory. You can use the `Example .env File` section as a template. The Docker setup will use these variables to configure the services.

2.  **Build and Start Services**: Run the following command from the project root. This will build the Docker images for the frontend and backend, create the database, and start all services.
    ```bash
    sudo docker-compose up --build
    ```

3.  **Run Database Migrations**: The first time you start the application, the database will be empty. The new configuration automatically runs migrations on startup, so you no longer need to do this manually.

After these steps, the application will be running and accessible at `http://localhost`.

### Everyday Usage

-   **Start all services**:
    ```bash
    sudo docker-compose up
    ```

-   **Stop all services**:
    ```bash
    sudo docker-compose down
    ```

### Helpful Docker Commands

-   **Rebuild and Start**: If you make changes to the `Dockerfile` or want to force a rebuild of your images:
    ```bash
    sudo docker-compose up --build
    ```

-   **View Logs**: To view the logs from all running services in real-time:
    ```bash
    sudo docker-compose logs -f
    ```
    To follow the logs for a specific service (e.g., the backend):
    ```bash
    sudo docker-compose logs -f backend
    ```

-   **Run Management Commands**: To run any Django `manage.py` command inside the backend container (e.g., to create a superuser):
    ```bash
    sudo docker-compose exec backend python manage.py createsuperuser
    ```

-   **Clean Up Unused Images**: To safely remove old, dangling images and free up disk space:
    ```bash
    sudo docker image prune
    ```

---

## 🚀 Running Tests

Run all backend tests using `pytest`:
```bash
pytest
```

Tests are also executed automatically via GitHub Actions on push and pull request events.

---

# ────────────────
# AI Agents Overview & Setup
# ────────────────

## Available Agents

- **SummarizerAgent**: Summarizes text using OpenAI.
- **QAPairAgent**: Answers questions and can store Q&A pairs.
- **EmailAgent**: Summarizes, drafts, and analyzes emails.
- **ExcelAgent**: Suggests formulas, summarizes, and analyzes spreadsheet data.
- **TeamsAgent**: Connects to Microsoft Teams/Outlook to create calendar events for maintenance, surveys, etc. Requires Microsoft Azure app registration.

## How to Set Up Each Agent

### 1. General Agents (Summarizer, QA, Email, Excel)
- **Requirement**: An OpenAI API key in your `.env` file:
  ```
  OPENAI_API_KEY=your-openai-key
  ```
- **Usage**: Interact with these agents through the web UI or via the `/api/agent/respond/` endpoint.

### 2. TeamsAgent (Microsoft Teams/Calendar Integration)
- **Requirements**:
  - Register an application in the Azure Portal (Azure Active Directory > App registrations).
  - Add the following credentials to your `.env` file:
    - `MS_CLIENT_ID`
    - `MS_CLIENT_SECRET`
    - `MS_TENANT_ID`
    - `MS_REDIRECT_URI` (e.g., `http://localhost:8000/msauth/callback/`)
  - Install the `O365` Python package: `pip install O365`
- **First Run**:
  - The first time you use the TeamsAgent, you will be prompted to authenticate in a browser. This will save a token file for future sessions.
- **Usage**:
  - Send a prompt with keywords like "maintenance," "survey," or "test running" through the UI.
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