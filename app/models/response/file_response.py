from datetime import datetime
from pydantic import BaseModel


class FileResponse(BaseModel):
    name: str
    mime_type: str
    type: str
    owner: str
    access_type: str
    created_at: datetime
    