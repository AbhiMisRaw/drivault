from datetime import datetime
from pydantic import BaseModel



class UserRegisterPayload(BaseModel):
    fullname: str
    email: str
    password: str


class UserProfileResponse(BaseModel):
    fullname: str
    email: str
    role: str
    created_at: datetime


