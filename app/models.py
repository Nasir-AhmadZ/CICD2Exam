from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint

class Base(DeclarativeBase):
    pass

class AuthorDB(Base)
    __tablename__ ="authors"
    id:mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(100))
    age:Mapped[int]=mapped_column(Integer,nullable=False)
    email:Mapped[str]=mapped_column(unique=True,nullable=False)
    year_started[int]=mapped_column(Integer(),nullable=False)
    books:Mapped[List["BookDB"]]=relationship(back_populates="author",cascade="all,delete-orphan")

class BookDB(Base)
    __tablename__ ="books"
    id:mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column
    pages:Mapped[int]=mapped_column
    author_id:Mapped[int]=mapped_column(ForeignKey("authors.id"))
    author:Mapped["AuthorDB"]=relationship(back_populates="books")