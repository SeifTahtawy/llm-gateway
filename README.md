# Multi-Provider LLM Gateway

A lightweight API gateway designed to provide a unified interface for interacting with multiple Large Language Model (LLM) providers.

The project aims to simplify communication with different LLM providers by introducing a common API, provider abstraction, and centralized request handling.

**Project Status:** Initial development — foundational application structure and development tooling implemented.

## Tech Stack

- **Python 3.12** — Programming language
- **FastAPI** — API framework
- **Uvicorn** — ASGI server
- **HTTPX** — HTTP client for provider communication
- **Pydantic** — Data validation and settings management
- **uv** — Python package and project management
- **Pytest** — Automated testing
- **Ruff** — Linting and formatting
- **MyPy** — Static type checking

## Current Features

- FastAPI application initialization.
- Modular API organization using `APIRouter`.
- Centralized application configuration using Pydantic Settings.
- Health-check endpoint.
- Automated endpoint testing using Pytest and FastAPI TestClient.
- Code quality checks using Ruff and MyPy.

## Project Structure

```text
llm-gateway/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   └── api/
│       ├── __init__.py
│       └── health.py
├── tests/
│   └── test_health.py
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
└── uv.lock
```

## Getting Started

### Prerequisites

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)

### Installation

Clone the repository:

```bash
git clone <repository-url>
cd llm-gateway
```

Install project dependencies:

```bash
uv sync
```

This installs the project dependencies using the versions recorded in `uv.lock`, including the development dependency group.

### Running the Application

Start the development server:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Health Check

**GET** `/api/health`

Returns the current health status of the application.

Example response:

```json
{
    "status": "healthy"
}
```

Expected HTTP status: `200 OK`.

## Testing

Run the automated test suite:

```bash
uv run pytest
```

## Code Quality

The project uses Ruff and MyPy to maintain code quality and type consistency.

### Linting

```bash
uv run ruff check .
```

Automatically fix supported linting issues:

```bash
uv run ruff check . --fix
```

### Formatting

Check formatting:

```bash
uv run ruff format --check .
```

Apply formatting:

```bash
uv run ruff format .
```

### Static Type Checking

```bash
uv run mypy app tests
```

## Roadmap

The following features are planned for future development:

- [ ] Unified API for LLM interactions.
- [ ] Common provider interface and provider abstraction.
- [ ] Integration with multiple LLM providers.
- [ ] Model routing.
- [ ] Normalized request and response schemas.
- [ ] Provider error handling and configurable timeouts.
- [ ] Server-Sent Events (SSE) streaming.
- [ ] Concurrent request handling.
- [ ] Backpressure management.
- [ ] Request cancellation.
- [ ] Authentication and API key management.
- [ ] Rate limiting.
- [ ] Observability, logging, and metrics.

Advanced functionality will be introduced incrementally as the foundational architecture develops.

## Development Philosophy

This project is being developed incrementally, with an emphasis on:

- Clean architecture and separation of concerns.
- Explicit interfaces and well-defined contracts.
- Asynchronous programming and efficient I/O.
- Automated testing and static analysis.
- Understanding engineering trade-offs and design decisions.