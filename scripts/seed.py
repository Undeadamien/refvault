#!/usr/bin/env python

import asyncio

import httpx
from httpx import ASGITransport
from sqlalchemy import text

from refvault.database import Base, engine
from refvault.main import app


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

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        users = [
            ("alice", "secret", False),
            ("bob", "secret", False),
            ("admin", "admin", True),
        ]

        tokens = {}
        for username, password, admin in users:
            r = await client.post(
                "/auth/register", json={"username": username, "password": password}
            )
            r.raise_for_status()
            tokens[username] = r.json()["access_token"]

            if admin:
                async with engine.begin() as conn:
                    await conn.execute(
                        text("UPDATE users SET is_admin = TRUE WHERE username = :name"),
                        {"name": username},
                    )

        image_specs = [
            (
                "Forest path",
                "https://picsum.photos/id/10/800/600",
                ["nature", "travel"],
                "alice",
            ),
            (
                "City skyline",
                "https://picsum.photos/id/28/800/600",
                ["architecture", "travel", "technology"],
                "alice",
            ),
            ("Coffee cup", "https://picsum.photos/id/42/800/600", ["food"], "bob"),
            (
                "Mountain lake",
                "https://picsum.photos/id/98/800/600",
                ["nature", "travel"],
                "alice",
            ),
            (
                "Laptop setup",
                "https://picsum.photos/id/180/800/600",
                ["technology"],
                "bob",
            ),
        ]

        for name, url, tags, owner in image_specs:
            r = await client.post(
                "/images/",
                json={"url": url, "name": name, "tags": tags},
                headers={"Authorization": f"Bearer {tokens[owner]}"},
            )
            r.raise_for_status()
            img = r.json()
            print(f"Created: {name}")

    print("Waiting for palette extraction...")
    await asyncio.sleep(5)

    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        for username, token in tokens.items():
            r = await client.get(
                "/images/",
                headers={"Authorization": f"Bearer {token}"},
            )
            r.raise_for_status()
            data = r.json()
            for img in data["items"]:
                status = f"palette={img['palette']}" if img["palette"] else "no palette"
                print(f"  [{username}] {img['name']}: {status}")


if __name__ == "__main__":
    asyncio.run(seed())
