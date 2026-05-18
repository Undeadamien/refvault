from sqladmin import ModelView

from src.models import Image, Tag, User

# todo: consider adding permissions
# https://smithyhq.github.io/sqladmin/configurations/#permissions


class AdminViewUser(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.images,
    ]


class AdminViewTag(ModelView, model=Tag):
    column_list = [
        Tag.id,
        Tag.name,
    ]


class AdminViewImage(ModelView, model=Image):
    column_list = [
        Image.id,
        Image.name,
        Image.url,
        Image.owner,
        Image.tags,
        Image.created_at,
    ]
