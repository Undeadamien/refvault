#!/usr/bin/env python

import os
from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import ImageCreate, ImageResponse

Base.metadata.create_all(bind=engine)

SERVER_ADDR = os.getenv("SERVER_ADDR", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

app = FastAPI(title="RefVault")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")


@app.get("/images", response_model=List[ImageResponse])
def get_images(db: Session = Depends(get_db)):
    images = db.query(models.Image).all()
    return images


@app.get("/image/{id}", response_model=ImageResponse)
def get_image(id: int, db: Session = Depends(get_db)):
    img = db.query(models.Image).filter(models.Image.id == id).first()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    return img


@app.post("/image", response_model=ImageResponse)
def post_image(payload: ImageCreate, db: Session = Depends(get_db)):
    img = models.Image(url=payload.url)
    db.add(img)
    db.commit()
    db.refresh(img)
    return img


@app.delete("/image/{id}")
def delete_image(id: int, db: Session = Depends(get_db)):
    img = db.query(models.Image).filter(models.Image.id == id).first()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(img)
    db.commit()
    return {"message": "deleted"}


def main():
    uvicorn.run("main:app", host=SERVER_ADDR, port=SERVER_PORT, reload=True)


if __name__ == "__main__":
    main()
