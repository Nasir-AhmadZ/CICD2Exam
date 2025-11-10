# app/main.py
from typing import Optional

from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Response
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import engine, SessionLocal
from app.models import Base, AuthorDB, BookDB
from app.schemas import AuthorCreate, AuthorRead, AuthorPATCH

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
        name=author.name,
        email=author.email,
        year_started=author.year_started)
    db.add(author)
    commit_or_rollback(db,"Author creation failed")
    return author

@app.get("/api/authors", response_model=list[AuthorRead])
def list_authors(db:Session=Depends(get_db)):
    stmt=select(AuthorDB).order_by(AuthorDB.id)
    result = db.execute(stmt)
    authors = result.scalars().all()
    return authors

@app.get("/api/authors/{author_id}",response_model=AuthorRead)
def get_author(db:Session=Depends(get_db)):
    author=db.get(AuthorDB,author_id)
    if not author:
        raise HTTPException(status_code=404,detail="Author not found")
    return author

@app.put("/api/authors/{author_id}",response_model=AuthorRead)
def update_author(payload:AuthorCreate,db:Session=Depends(get_db)):
    author=db.get(AuthorDB,author_id)
    if not author:
        raise HTTPException(status_code=404,detail="Author not found")
    
    for key, value in payload.model_dump().items():
        setattr(author,key,value)
    commit_or_rollback(db,"author update failed")
    db.refresh(author)
    return author 

@app.patch("/api/authors/{author_id}",response_model=AuthorPATCH,status_code=status.HTTP_201_CREATED)
def patch_author(payload:AuthorPATCH,db:Session=Depends(get_db)):
    author=db.get(AuthorDB,author_id)
    if not author:
        raise HTTPException(status_code=404,detail="Author not found")
    
    for key, value in payload.model_dump().items():
        setattr(author,key,value)
    commit_or_rollback(db,"author PATCH failed")
    db.refresh(author)
    return author  

'''@app.delete("/api/authors/{author_id}",status_code=204)
def delete_author(author_id:int,db:Session=Depends())->Response:
    author=db.get(AuthorDB,author_id)
    if not author:
        raise HTTPException(status_code=404,detail="Author not found")
    db.delete(author)
    db.commit()
    return Response(status=201)'''

