from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict

NameStr=Annotated[Str,StringConstraints(min_length=1,max_length=100)]
year_started_int=Annotated[Int,Ge(1899),Le(2101)]
pagesInt=Annotated[Int,Ge(1),Le(10000)]
TitleStr=Annotated[Str,StringConstraints(min_length=1,max_length=255)]

#creating author
class AuthorCreate(BaseModel):
    name:NameStr
    email:EmailStr
    year_started:year_started_int

class AuthorRead(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int
    Title:TitleStr
    email:EmailStr
    pages:pagesInt
    author_id:int