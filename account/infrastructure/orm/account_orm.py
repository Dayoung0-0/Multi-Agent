from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from datetime import datetime

from config.database.session import Base


class AccountORM(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    name = Column(String(50), nullable=False)
    status = Column(String(10), nullable=False, default="active")
    profile_image = Column(String(500), nullable=True)
    provider = Column(String(50), nullable=False, default="local")
    password = Column(String(255), nullable=True)
    nickname = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
            CheckConstraint(
                'username IS NOT NULL OR email IS NOT NULL',
                name='chk_username_email'
            ),
    )