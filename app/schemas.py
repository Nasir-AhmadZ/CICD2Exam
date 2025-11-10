from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict,conint

NameStr=Annotated[str,StringConstraints(min_length=1,max_length=100)]
#year_started_int=Annotated[int,ge=(1899),le=(2101)]
#pagesInt=Annotated[int,ge=(1),le=(10000)]
TitleStr=Annotated[str,StringConstraints(min_length=1,max_length=255)]

#creating author
class AuthorCreate(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    name:NameStr
    email:EmailStr
    year_started:conint(ge=1900,le=2100)

class AuthorPATCH(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    name:Optional[NameStr]=None
    email:Optional[EmailStr]=None
    year_started:Optional[conint(ge=1900,le=2100)]=None

class AuthorRead(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int
    Title:TitleStr
    email:EmailStr
    pages:conint(ge=1,le=10000)
    author_id:int