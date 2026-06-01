#!/usr/bin/env python


import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

from refvault.admin import AdminAuth, AdminViewImage, AdminViewTag, AdminViewUser
from refvault.config import settings
from refvault.database import engine
from refvault.limiter import limiter
from refvault.routes import auth, images, tags

app = FastAPI(title="RefVault")
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.state.limiter = limiter

app.include_router(auth.router)
app.include_router(images.router)
app.include_router(tags.router)

settings.upload_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

admin = Admin(app, engine, authentication_backend=AdminAuth(settings.secret_key))
admin.add_view(AdminViewUser)
admin.add_view(AdminViewTag)
admin.add_view(AdminViewImage)


def main():
    uvicorn.run(
        "refvault.main:app",
        host=settings.server_addr,
        port=settings.server_port,
        reload=settings.reload,
    )


if __name__ == "__main__":
    main()
