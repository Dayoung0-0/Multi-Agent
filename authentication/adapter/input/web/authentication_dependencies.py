from typing import Optional
from fastapi import Cookie, HTTPException, status

from config.redis_config import get_redis
from account.application.usecase.account_usecase import AccountUseCase
from account.domain.account import Account

redis_client = get_redis()
account_usecase = AccountUseCase.getInstance()


# def _authenticate_with_google(access_token: str) -> Account:

def _authenticate_with_local() -> Account:
    """
    로컬 로그인 인증 처리 (JWT 토큰 등)
    """

def _authenticate_with_kakao() -> Account:
    """
    다른 소셜 로그인 인증 처리 (Facebook, Kakao, Naver 등)
    """


def get_current_user(session_id: Optional[str] = Cookie(None)) -> Account:
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please login first."
        )

    # Redis에서 인증 데이터 가져오기
    auth_data = redis_client.get(session_id)
    if not auth_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please login again."
        )

