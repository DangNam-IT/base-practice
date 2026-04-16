from datetime import datetime, UTC
from typing import Optional, Annotated
from pydantic import BaseModel, Field
class AuthorBase(BaseModel):
    name: Annotated[str, Field(..., min_length=1, max_length=100)]
    bio: Optional[str] = None
 
class AuthorUpdate(BaseModel):
    name: Optional[Annotated[str, Field(None, min_length=1, max_length=100)]] = None
    bio: Optional[str] = None

class AuthorResponse(AuthorBase):
    id: int
    name: str
    bio: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
 