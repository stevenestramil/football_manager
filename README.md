# Football Manager API

A REST API to manage football teams and players, built with FastAPI.

## Install dependencies

First Install uv package manager and then: 

```bash
uv sync
```

## Run the app

```bash
uv run fastapi dev src/main.py --reload
```

The API will be available at http://localhost:8000.  
Interactive docs at http://localhost:8000/docs.

## Run tests

```bash
uv run pytest -v
```

## Lint and format

```bash
uv run ruff check .
uv run ruff format .
```
