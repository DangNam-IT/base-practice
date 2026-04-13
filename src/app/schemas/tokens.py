from typing import Optional 
from pydantic import BaseModel
 
 
# ─────────────────────────────────────────────
# AUTH / TOKEN
# ─────────────────────────────────────────────
 
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
 
 
class TokenData(BaseModel):
    """Payload lưu trong JWT."""
    username: Optional[str] = None
    role: str = "user"
 