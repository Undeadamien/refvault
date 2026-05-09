#!/usr/bin/env python

import uvicorn
from fastapi import FastAPI

from src.config import settings
from src.routes import images, tags

app = FastAPI(title="RefVault")
app.include_router(images.router)
app.include_router(tags.router)


def main():
    uvicorn.run(
        "main:app", host=settings.server_addr, port=settings.server_port, reload=True
    )


if __name__ == "__main__":
    main()
