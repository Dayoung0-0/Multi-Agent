from pydantic import BaseModel
from typing import Optional


class UpdateAccountRequest(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    profile_image: Optional[str] = None
    nickname: Optional[str] = None