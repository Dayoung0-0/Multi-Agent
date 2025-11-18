from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AccountResponse(BaseModel):
    id: int
    email: str
    name: str
    profile_image: Optional[str]
    provider: str
    created_at: datetime
    updated_at: datetime
