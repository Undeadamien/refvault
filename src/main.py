#!/usr/bin/env python

import os

import uvicorn
from fastapi import FastAPI

from src.routes import images, tags

SERVER_ADDR = os.getenv("SERVER_ADDR", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))


app = FastAPI(title="RefVault")
app.include_router(images.router)
app.include_router(tags.router)


def main():
    uvicorn.run("main:app", host=SERVER_ADDR, port=SERVER_PORT, reload=True)


if __name__ == "__main__":
    main()
