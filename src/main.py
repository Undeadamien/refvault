#!/usr/bin/env python

import os
from contextlib import asynccontextmanager
from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
from database import Base, engine, get_db
from schemas import ImageCreate, ImageResponse

SERVER_ADDR = os.getenv("SERVER_ADDR", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="RefVault", lifespan=lifespan)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.get("/images", response_model=List[ImageResponse])
async def get_images(db: AsyncSession = Depends(get_db)):
    images = await db.execute(select(models.Image))
    return images.scalars().all()


@app.get("/image/{id}", response_model=ImageResponse)
async def get_image(id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(models.Image).where(models.Image.id == id))
    img = res.scalar_one_or_none()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    return img


@app.post("/image", response_model=ImageResponse)
async def post_image(payload: ImageCreate, db: AsyncSession = Depends(get_db)):
    img = models.Image(url=payload.url)
    db.add(img)
    await db.commit()
    await db.refresh(img)
    return img


@app.delete("/image/{id}")
async def delete_image(id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(models.Image).where(models.Image.id == id))
    img = res.scalar_one_or_none()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    await db.delete(img)
    await db.commit()
    return {"message": "deleted"}


def main():
    uvicorn.run("main:app", host=SERVER_ADDR, port=SERVER_PORT, reload=True)


if __name__ == "__main__":
    main()
