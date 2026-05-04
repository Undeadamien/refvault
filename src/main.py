#!/usr/bin/env python

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from database import Base, engine

Base.metadata.create_all(bind=engine)

SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 8000

app = FastAPI(title="RefVault")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")


def main():
    uvicorn.run("main:app", host=SERVER_ADDR, port=SERVER_PORT, reload=True)


if __name__ == "__main__":
    main()
