# 🧠 AIAgent

![AIAgent](/frontend/public/img/Baner.png?raw=true)

**AIAgent** is a full-stack framework for building and managing intelligent, task-oriented agents. It combines a powerful Django backend with a modern React frontend, providing a robust foundation for automating workflows and interacting with AI models.

This project is designed for extensibility, allowing you to create domain-specific assistants—such as social media managers, file analyzers, or enterprise support bots—with a complete user interface.

## 🌟 Features

-   **Modular Backend**: Reusable Django apps for core services, agents, and scheduling.
-   **React Frontend**: A dynamic and responsive user interface for interacting with the AI agents.
-   **LLM Integration**: Seamlessly connect with OpenAI for dynamic prompt handling.
-   **REST APIs**: Communicate between the frontend and backend using Django REST Framework.
-   **Pre-built Agents**: Includes agents for summarization, Q&A, email, Excel, and Teams calendar integration.
-   **Custom Commands**: Automate tasks with custom Django management commands.
-   **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions.
-   **Dockerized Environment**: Run the entire application with a single command using Docker Compose.

## 🚀 Getting Started

### Prerequisites

-   [Docker](https://docs.docker.com/get-docker/)
-   [Docker Compose](https://docs.docker.com/compose/install/)
-   [Git](https://git-scm.com/downloads)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Ghosts6/ai-platform
    cd AIAgent
    ```

2.  **Create a `.env` file** in the `ai_agent` directory. Use the `Example .env File` section as a template.

3.  **Build and start the services**:
    ```bash
    sudo docker-compose up --build
    ```

The application will be available at `http://localhost`.

## USAGE

1.  **Open the application** in your browser at `http://localhost`.
2.  **Explore the available agents** on the "Agents" page.
3.  **Select an agent** to interact with.
4.  **Enter a prompt** and receive a response from the agent.
5.  **View your conversation history** on the "Agent History" page.

## 🛠️ Technologies & Architecture

-   **Backend**: Python 3.11+, Django 4.x, Django REST Framework
-   **Frontend**: React, React Router, Axios, Tailwind CSS
-   **AI & LLM**: OpenAI API (ChatGPT, GPT-4)
-   **Containerization**: Docker, Docker Compose
-   **Database**: PostgreSQL (SQLite supported for development)
-   **Background Tasks**: Celery with Redis broker, APScheduler for timed jobs
-   **Testing**: pytest, pytest-django, GitHub Actions CI pipeline
-   **Environment Management**: `.env` with `python-dotenv`
-   **Static Handling**: WhiteNoise for serving static files in production

## 📁 Project Structure

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

## 🤖 AI & LLM Features

This project is not just a standard web application; it's a platform for building and experimenting with advanced AI and Large Language Model (LLM) features. Here's an overview of the AI-powered capabilities you'll find in this project.

### Core Concepts

*   **Agent-Based Architecture**: The entire platform is built around the concept of autonomous agents. Each agent is a specialized AI model designed to perform a specific set of tasks. This modular approach allows for easy extension and customization.

*   **Reinforcement Learning (RL)**: We leverage RL techniques to train our agents to improve their performance over time. By learning from user interactions and feedback, the agents become more efficient and accurate in their responses.

*   **Retrieval-Augmented Generation (RAG)**: To provide more accurate and context-aware responses, we use a RAG-based approach. This allows the agents to retrieve information from a knowledge base and use it to augment their generated responses.

### RAGFlow and Elasticsearch

To implement our RAG-based architecture, we use a combination of **RAGFlow** and **Elasticsearch**.

*   **RAGFlow**: RAGFlow is a powerful open-source engine for building RAG-based applications. We use it to manage the entire RAG workflow, from data ingestion and processing to retrieval and generation.

*   **Elasticsearch**: Elasticsearch is a distributed, RESTful search and analytics engine. We use it as our primary knowledge base, storing and indexing all the information that our agents need to access.

### AI Agents Overview & Setup

### Available Agents

-   **SummarizerAgent**: Summarizes text using OpenAI.
-   **QAPairAgent**: Answers questions and can store Q&A pairs.
-   **EmailAgent**: Summarizes, drafts, and analyzes emails.
-   **ExcelAgent**: Suggests formulas, summarizes, and analyzes spreadsheet data.
-   **TeamsAgent**: Connects to Microsoft Teams/Outlook to create calendar events for maintenance, surveys, etc. Requires Microsoft Azure app registration.

### How to Set Up Each Agent

#### 1. General Agents (Summarizer, QA, Email, Excel)

-   **Requirement**: An OpenAI API key in your `.env` file:
    ```
    OPENAI_API_KEY=your-openai-key
    ```
-   **Usage**: Interact with these agents through the web UI or via the `/api/agent/respond/` endpoint.

#### 2. TeamsAgent (Microsoft Teams/Calendar Integration)

-   **Requirements**:
    -   Register an application in the Azure Portal (Azure Active Directory > App registrations).
    -   Add the following credentials to your `.env` file:
        -   `MS_CLIENT_ID`
        -   `MS_CLIENT_SECRET`
        -   `MS_TENANT_ID`
        -   `MS_REDIRECT_URI` (e.g., `http://localhost:8000/msauth/callback/`)
    -   Install the `O365` Python package: `pip install O365`
-   **First Run**:
    -   The first time you use the TeamsAgent, you will be prompted to authenticate in a browser. This will save a token file for future sessions.
-   **Usage**:
    -   Send a prompt with keywords like "maintenance," "survey," or "test running" through the UI.
    -   The agent will create a calendar event in your default Teams/Outlook calendar.

## 📝 Example .env File

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

## ✅ Running Tests

Run all backend tests using `pytest`:

```bash
pytest
```

Tests are also executed automatically via GitHub Actions on push and pull request events.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## 📄 License

This project is licensed under the MIT License.

## 🎥 Demo

[AiAgent.webm](https://github.com/user-attachments/assets/aa83cf43-9d50-4db6-959d-2ca0f4fd9040)

