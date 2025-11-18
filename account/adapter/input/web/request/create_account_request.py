from pydantic import BaseModel
from typing import Optional


class CreateAccountRequest(BaseModel):
    username: Optional[str] = None
    email: str
    name: str
    profile_image: Optional[str] = None
    provider: str = "local"
    status: str = "active"
    password: Optional[str] = None
    nickname: Optional[str] = None
