from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from schemas.authors import AuthorResponse
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, max_length=20)
    is_available: bool = True
    author_id: int
 
 
class BookCreate(BookBase):
    pass
 
 
class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, max_length=20)
    is_available: Optional[bool] = None
    author_id: Optional[int] = None
 
 
class BookResponse(BookBase):
    id: int
    title: Optional[str]= Field(..., min_length=1, max_length=200)
    created_at: datetime
    author: AuthorResponse
 
    model_config = {"from_attributes": True}