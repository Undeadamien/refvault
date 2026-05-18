#!/usr/bin/env python

import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from src.admin import AdminViewImage, AdminViewTag, AdminViewUser
from src.config import settings
from src.database import engine
from src.routes import auth, images, tags

app = FastAPI(title="RefVault")
app.include_router(auth.router)
app.include_router(images.router)
app.include_router(tags.router)

admin = Admin(app, engine)
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
