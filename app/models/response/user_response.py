from datetime import datetime
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    fullname: str
    email: str
    is_active: bool
    role: str
    created_at: datetime