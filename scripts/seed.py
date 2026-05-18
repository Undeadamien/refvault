#!/usr/bin/env python

import asyncio

from src.database import Base, SessionLocal, engine
from src.models import Image, Tag, User, image_tags
from src.services.auth import hash_password


async def seed():
    answer = input(
        "This script will replace the existing database, do you want to proceed? [y/n]"
    )
    if answer != "y":
        print("Aborting")
        exit()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        users = [
            User(username="alice", hashed_password=hash_password("secret")),
            User(username="bob", hashed_password=hash_password("secret")),
            User(
                username="admin", hashed_password=hash_password("admin"), is_admin=True
            ),
        ]
        db.add_all(users)
        await db.flush()

        tags = [
            Tag(name="nature"),
            Tag(name="architecture"),
            Tag(name="food"),
            Tag(name="travel"),
            Tag(name="technology"),
        ]
        db.add_all(tags)
        await db.flush()

        images = [
            Image(
                url="https://picsum.photos/id/10/800/600",
                name="Forest path",
                user_id=users[0].id,
            ),
            Image(
                url="https://picsum.photos/id/28/800/600",
                name="City skyline",
                user_id=users[0].id,
            ),
            Image(
                url="https://picsum.photos/id/42/800/600",
                name="Coffee cup",
                user_id=users[1].id,
            ),
            Image(
                url="https://picsum.photos/id/98/800/600",
                name="Mountain lake",
                user_id=users[0].id,
            ),
            Image(
                url="https://picsum.photos/id/180/800/600",
                name="Laptop setup",
                user_id=users[1].id,
            ),
        ]
        db.add_all(images)
        await db.flush()

        tag_map = {t.name: t for t in tags}
        image_tag_pairs = [
            (images[0], ["nature", "travel"]),
            (images[1], ["architecture", "travel", "technology"]),
            (images[2], ["food"]),
            (images[3], ["nature", "travel"]),
            (images[4], ["technology"]),
        ]
        for img, tag_names in image_tag_pairs:
            for name in tag_names:
                await db.execute(
                    image_tags.insert().values(image_id=img.id, tag_id=tag_map[name].id)
                )

        await db.commit()


if __name__ == "__main__":

    asyncio.run(seed())
