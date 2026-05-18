from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from starlette.requests import Request

from src.database import SessionLocal
from src.models import Image, Tag, User
from src.services.auth import verify_password


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username: str = str(form.get("username"))
        password: str = str(form.get("password"))

        async with SessionLocal() as db:
            res = await db.execute(select(User).where(User.username == username))
            user = res.scalar_one_or_none()
            if (
                user
                and verify_password(password, user.hashed_password)
                and user.is_admin
            ):
                request.session.update({"user_id": user.id, "username": username})
                return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return "user_id" in request.session


class AdminViewUser(ModelView, model=User):
    column_list = [User.id, User.username, User.images, User.is_admin]
    column_details_exclude_list = [User.hashed_password]
    column_sortable_list = [User.id, User.is_admin]
    form_excluded_columns = [User.hashed_password]


class AdminViewTag(ModelView, model=Tag):
    column_list = [Tag.id, Tag.name]
    column_sortable_list = [Tag.id]


class AdminViewImage(ModelView, model=Image):
    column_list = [
        Image.id,
        Image.name,
        Image.url,
        Image.user_id,
        Image.owner,
        Image.tags,
        Image.created_at,
    ]
    column_sortable_list = [Image.id, Image.url, Image.user_id, Image.created_at]
