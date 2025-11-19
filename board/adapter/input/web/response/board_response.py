from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class BoardResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    author_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
