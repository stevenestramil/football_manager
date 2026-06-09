# Football Manager API

A REST API to manage football teams and players, built with FastAPI.

## Install dependencies

First Install uv package manager and then: 

```bash
uv sync
```

## Database migrations

The app uses SQLite (`football.db`) with Alembic for schema migrations.

Apply all pending migrations before running the app for the first time:

```bash
uv run alembic upgrade head
```

After changing an ORM model in `src/core/db_models.py`, generate a new migration:

```bash
uv run alembic revision --autogenerate -m "describe your change"
uv run alembic upgrade head
```

Other useful commands:

```bash
uv run alembic current      # show currently applied revision
uv run alembic history      # show migration history
uv run alembic downgrade -1 # revert the last migration
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
