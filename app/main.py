from fastapi import FastAPI
from .db import engine
from .orm import Base
from .api import users, team, pull_request

app = FastAPI(title="PR Reviewer Assignment Service")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router, prefix="/users")
app.include_router(team.router, prefix="/team")
app.include_router(pull_request.router, prefix="/pullRequest")
