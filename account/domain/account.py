from typing import Optional
from datetime import datetime


class Account:
    def __init__(
        self,
        username: str,
        email: str,
        name: str,
        status: str,
        profile_image: Optional[str] = None,
        provider: str = "local",
        password: Optional[str] = None,
        nickname: Optional[str] = None
    ):
        self.id: Optional[int] = None
        self.username = username
        self.email = email
        self.name = name
        self.status = status # 나중에 enum으로?
        self.profile_image = profile_image
        self.provider = provider
        self.password = password
        self.nickname = nickname
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()

    def update(self, name: str, status: str, profile_image: Optional[str] = None):
        if name:
            self.name = name
        if profile_image:
            self.profile_image = profile_image
        if status:
            self.status = status
        if name or profile_image:
            self.updated_at = datetime.utcnow()
