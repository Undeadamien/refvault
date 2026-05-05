#!/usr/bin/env python

import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database import Base, engine
from routes import images, tags

SERVER_ADDR = os.getenv("SERVER_ADDR", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="RefVault", lifespan=lifespan)
app.include_router(images.router)
app.include_router(tags.router)


def main():
    uvicorn.run("main:app", host=SERVER_ADDR, port=SERVER_PORT, reload=True)


if __name__ == "__main__":
    main()
