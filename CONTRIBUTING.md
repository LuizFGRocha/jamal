# Contributing to Jamal

## Setup

1. Fork the repository and clone it locally.
2. Create a virtual environment and install development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest tests/ -v
```

## Code Style

- Follow PEP 8 conventions.
- Use type hints for all public functions.
- Keep functions small and focused — prefer extracting helpers over deep nesting.

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `ci:`, `chore:`

## Pull Requests

1. Create a feature branch from `main` (e.g., `feature/my-feature` or `fix/issue-42`).
2. Make small, focused commits — one logical change per commit.
3. Ensure all tests pass: `pytest tests/ -v`.
4. Write a clear PR description explaining the *why* behind the change.
