import re
from pydantic import BaseModel, Field, field_validator
from typing import Optional, TypeVar, Generic, List
from datetime import datetime
from app.schemas.authors import AuthorResponse

T = TypeVar("T")
 
class PaginatedResponse(BaseModel, Generic[T]):
    """Generic pagination wrapper dùng cho mọi list endpoint."""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
 

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, max_length=20)
    is_available: bool = True
    author_id: int

 
 
class BookCreate(BookBase):
    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: Optional[str]) -> Optional[str]:
        return _cleaned_isbn(v)
 

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, max_length=20)
    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: Optional[str]) -> Optional[str]:
        return _cleaned_isbn(v)
    is_available: Optional[bool] = None
    author_id: Optional[int] = None
 
 
class BookResponse(BookBase):
    id: int
    title: Optional[str]= Field(..., min_length=1, max_length=200)
    created_at: datetime
    updated_at: datetime
    author: AuthorResponse
 
    model_config = {"from_attributes": True}

def _cleaned_isbn(v: Optional[str]) -> Optional[str]:
    if v is None:
        return v
    cleaned = re.sub(r"[\s\-]", "", v)  # Remove dashes
    if not cleaned.isdigit():
        raise ValueError("ISBN chỉ được chứa số, dấu cách hoặc gạch ngang")
    if len(cleaned) not in (10, 13):
        raise ValueError("ISBN phải có 10 hoặc 13 số")
    return cleaned