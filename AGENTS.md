# AGENTS.md

## Project Overview
- **Project name**: FastAPI Hello World Server
- **Project type**: REST API Backend
- **Core functionality**: FastAPI server with a `/hello` endpoint returning "Hello, World!"
- **Python version**: 3.10+

## Build/Lint/Test Commands

### Installation
```bash
uv sync
```

### Running the Server
```bash
uv run uvicorn main:app --reload
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

### Linting
```bash
ruff check .
```

### Formatting
```bash
ruff format .
```

### Type Checking
```bash
mypy .
```

### All Checks (CI)
```bash
ruff check . && ruff format . && mypy . && pytest
```

## Code Style Guidelines

### Imports
- Use absolute imports (e.g., `from app.routers import hello`)
- Group imports in this order: standard library, third-party, local application
- Use `isort` or let `ruff` handle import sorting

### Formatting
- Use **Ruff** for formatting (follows Black-compatible rules)
- Line length: 88 characters (default)
- Use trailing commas

### Types
- Use **type hints** for all function arguments and return values
- Use `Pydantic` models for request/response validation
- Run **mypy** before committing

### Naming Conventions
- **Files**: snake_case (e.g., `user_service.py`)
- **Classes**: PascalCase (e.g., `UserService`)
- **Functions/variables**: snake_case (e.g., `get_user_by_id`)
- **Constants**: SCREAMING_SNAKE_CASE
- **API endpoints**: kebab-case in URL path, snake_case in code

### Error Handling
- Use HTTPException for API errors with appropriate status codes
- Create custom exception handlers for consistent error responses
- Always return JSON-serializable error responses

### FastAPI Best Practices
- Use dependency injection for shared logic
- Define Pydantic models for request/response schemas
- Use async/await for I/O-bound operations
- Add OpenAPI schema descriptions (summary, description, response_model)
- Use status codes: 200 (OK), 201 (Created), 404 (Not Found), 422 (Validation), 500 (Server Error)

### Testing
- Use **pytest** with `pytest-asyncio` for async tests
- Use **httpx** TestClient for endpoint testing
- Place tests in `tests/` directory, mirror project structure
- Name test files: `test_<module>.py`
- Test naming: `test_<description>_<expected_behavior>`

### Project Structure
```
.
├── main.py              # FastAPI app entry point
├── routers/             # API route handlers
│   └── hello.py
├── schemas/             # Pydantic models
├── services/           # Business logic
├── tests/               # Test files
├── requirements.txt     # Dependencies
├── .ruff.toml           # Ruff configuration
└── AGENTS.md            # This file
```

### Dependencies (typical)
- fastapi
- uvicorn
- pydantic
- pytest
- pytest-asyncio
- httpx
- ruff
- mypy
