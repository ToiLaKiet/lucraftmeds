# LucraftMeds Backend

The backend contains the medical document-processing and RAG components used by
LucraftMeds.

## Requirements

- [uv](https://docs.astral.sh/uv/)
- Python `3.12+`

The required Python version is declared in `.python-version` and
`pyproject.toml`. When no compatible interpreter is available, uv can install
one automatically.

## Set Up the Environment

Run the following commands from the repository root:

```bash
cd backend
uv sync
```

`uv sync` creates the local `.venv` and installs the exact dependency versions
recorded in `uv.lock`. Activating `.venv` manually is not required; backend
commands should be executed through `uv run`.

Create `.env` inside this directory and add the required local environment
variables. Do not commit secrets to the repository.

## Run Tests

From the `backend` directory, run the complete test suite with:

```bash
uv run python -m pytest
```

Using `python -m pytest` through `uv run` ensures that both Python and pytest
come from the project's `.venv`, rather than a system-wide installation.

Run a single test file:

```bash
uv run python -m pytest tests/test_chunking.py
```

Run tests with verbose output:

```bash
uv run python -m pytest -v
```

## Manage Dependencies

Add a runtime dependency:

```bash
uv add <package>
```

Add a development-only dependency such as a test or linting tool:

```bash
uv add --dev <package>
```

After changing dependencies, commit both `pyproject.toml` and `uv.lock`.
