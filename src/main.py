#!/usr/bin/env python

import uvicorn
from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

from src.admin import AdminAuth, AdminViewImage, AdminViewTag, AdminViewUser
from src.config import settings
from src.database import engine
from src.routes import auth, images, tags

app = FastAPI(title="RefVault")
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.include_router(auth.router)
app.include_router(images.router)
app.include_router(tags.router)

admin = Admin(app, engine, authentication_backend=AdminAuth(settings.secret_key))
admin.add_view(AdminViewUser)
admin.add_view(AdminViewTag)
admin.add_view(AdminViewImage)


def main():
    uvicorn.run(
        "src.main:app",
        host=settings.server_addr,
        port=settings.server_port,
        reload=settings.reload,
    )


if __name__ == "__main__":
    main()
