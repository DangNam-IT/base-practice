from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = None
 
class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    bio: Optional[str] = None

class AuthorResponse(AuthorBase):
    id: int
    name: str
    bio: Optional[str] = None
    created_at: datetime
    model_config = {"from_attributes": True}
 