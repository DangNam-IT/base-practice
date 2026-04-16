from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Annotated

class UserCreate(BaseModel):
    username: Annotated[str, Field(..., min_length=3, max_length=50)]
    password: Annotated[str, Field(..., min_length=6, max_length=100)]
 
    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("Username chỉ chứa chữ cái, số và dấu gạch dưới")
        return v.lower()
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime
    model_config = {"from_attributes": True}