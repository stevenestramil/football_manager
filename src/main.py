from fastapi import FastAPI
from api.routes import players, teams

app = FastAPI()

app.include_router(players.router)
app.include_router(teams.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
