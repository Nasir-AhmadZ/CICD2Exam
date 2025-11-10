# app/main.py
from typing import Optional

from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import engine, SessionLocal
from app.models import Base
from app.schemas import AuthorCreate, AuthorRead  

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (dev/exam). Prefer Alembic in production.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

def commit_or_rollback(db:Session,error_msg:str):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,detail=error_msg)
        
# ---- Health ----
@app.get("/health")
def health():
    return {"status": "ok"}

# ---- Author ----]

@app.post("/api/authors", response_model=AuthorRead)
def create_author(author:AuthorCreate,db:Session=Depends(get_db)):
    author = AuthorDB(
        name=author.name
        email=author.email
        year_started=author.year_started
    )
    db.add(author)
    commit_or_rollback(db,"Author creation failed")
    return author

@app.get("/api/authors", response_model=list[AuthorRead])