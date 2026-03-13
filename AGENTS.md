# AGENTS.md

## Project Overview
- **Project name**: HelloWorld QA API
- **Project type**: Full-stack Web Application (FastAPI + React)
- **Core functionality**: Question answering API using DistilBERT model, with a React frontend
- **Python version**: 3.10+

## Project Structure
```
.
├── main.py                  # FastAPI application entry point
├── pyproject.toml           # Python dependencies and tool config
├── uv.lock                  # Locked dependencies
├── AGENTS.md                # This file
├── Dockerfile               # Docker container definition
├── deploy.sh                # Deployment script
├── .dockerignore            # Docker ignore file
├── terraform/               # Infrastructure as code
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── frontend/                # React frontend application
│   ├── package.json
│   ├── vite.config.js
│   ├── eslint.config.js
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   ├── index.css
│   │   └── assets/
│   └── public/
└── tests/                   # Test files
    ├── test_main.py
    └── conftest.py
```

## Build/Lint/Test Commands

### Installation (Python)
```bash
uv sync
```

### Installation (Frontend)
```bash
cd frontend && npm install
```

### Running the Server
```bash
uv run uvicorn main:app --reload --port 8000
```

### Running the Frontend
```bash
cd frontend && npm run dev
```

### Running Tests
```bash
pytest
```

### Run a Single Test
```bash
pytest tests/test_main.py::test_hello_endpoint
pytest -k "test_hello"
```

### Linting (Python)
```bash
ruff check .
```

### Formatting (Python)
```bash
ruff format .
```

### Type Checking (Python)
```bash
mypy .
```

### Linting (Frontend)
```bash
cd frontend && npm run lint
```

### Building Frontend
```bash
cd frontend && npm run build
```

### All Checks (CI)
```bash
ruff check . && ruff format . && mypy . && pytest
```

## Dependencies

### Python (Core)
- fastapi
- uvicorn
- pydantic
- torch
- transformers

### Python (Dev)
- pytest
- pytest-asyncio
- httpx
- ruff
- mypy

### Frontend
- react
- react-dom
- vite

## Code Style Guidelines

### Python

#### Imports
- Use absolute imports (e.g., `from app.routers import hello`)
- Group imports in this order: standard library, third-party, local application
- Use `ruff` for import sorting

#### Formatting
- Use **Ruff** for formatting (follows Black-compatible rules)
- Line length: 88 characters (default)
- Use trailing commas

#### Types
- Use **type hints** for all function arguments and return values
- Use `Pydantic` models for request/response validation
- Run **mypy** before committing

#### Naming Conventions
- **Files**: snake_case (e.g., `user_service.py`)
- **Classes**: PascalCase (e.g., `UserService`)
- **Functions/variables**: snake_case (e.g., `get_user_by_id`)
- **Constants**: SCREAMING_SNAKE_CASE
- **API endpoints**: kebab-case in URL path, snake_case in code

#### Error Handling
- Use HTTPException for API errors with appropriate status codes
- Create custom exception handlers for consistent error responses
- Always return JSON-serializable error responses

#### FastAPI Best Practices
- Use dependency injection for shared logic
- Define Pydantic models for request/response schemas
- Use async/await for I/O-bound operations
- Add OpenAPI schema descriptions (summary, description, response_model)
- Use status codes: 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found), 422 (Validation), 500 (Server Error)

### Testing
- Use **pytest** with `pytest-asyncio` for async tests
- Use **httpx** TestClient for endpoint testing
- Place tests in `tests/` directory, mirror project structure
- Name test files: `test_<module>.py`
- Test naming: `test_<description>_<expected_behavior>`

### Frontend (React)

#### General
- Use functional components with hooks
- Use ES6+ features
- Use CSS modules or CSS-in-JS for styling

#### Naming
- **Components**: PascalCase (e.g., `UserProfile.jsx`)
- **Files**: PascalCase for components, camelCase for utilities
- **CSS**: Match component name (e.g., `UserProfile.css`)

## API Endpoints

### GET /
- Returns HTML response
- Used for health check

### POST /agent
- **Request Body**: `{ "question": string, "context": string }`
- **Response**: `{ "answer": string, "score": float, "start": int, "end": int }`
- Uses DistilBERT model for question answering
- Supports MPS (Apple Silicon) GPU acceleration
