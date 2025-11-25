from fastapi import FastAPI
from .db import engine
from .orm import Base

app = FastAPI(title="PR Reviewer Assignment Service")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
