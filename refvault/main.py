#!/usr/bin/env python
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

from alembic import command
from alembic.config import Config
from refvault.admin import AdminAuth, AdminViewImage, AdminViewTag, AdminViewUser
from refvault.config import settings
from refvault.database import engine
from refvault.limiter import limiter
from refvault.routes import auth, images, tags
from refvault.services.cache import close as cache_close
from refvault.services.cache import init as cache_init

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await cache_init()
    yield
    await cache_close()


app = FastAPI(title="RefVault", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.state.limiter = limiter

app.include_router(auth.router)
app.include_router(images.router)
app.include_router(tags.router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health():
    return {"status": "ok"}


settings.upload_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

try:
    admin = Admin(app, engine, authentication_backend=AdminAuth(settings.secret_key))
    admin.add_view(AdminViewUser)
    admin.add_view(AdminViewTag)
    admin.add_view(AdminViewImage)
except Exception as e:
    logger.warning("Admin panel not available: %s", e)


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def main():
    run_migrations()
    uvicorn.run(
        "refvault.main:app",
        host=settings.server_addr,
        port=settings.server_port,
        reload=settings.reload,
    )


if __name__ == "__main__":
    main()
