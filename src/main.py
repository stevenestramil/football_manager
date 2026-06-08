from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import players, teams
from core.db import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(players.router)
app.include_router(teams.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
