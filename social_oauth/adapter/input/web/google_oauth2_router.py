import uuid
from fastapi import APIRouter, Response, Request, Cookie
from fastapi.responses import RedirectResponse

from account.application.usecase.account_usecase import AccountUseCase
from account.infrastructure.repository.account_repository_impl import AccountRepositoryImpl
from config.redis_config import get_redis
from social_oauth.application.usecase.google_oauth2_usecase import GoogleOAuth2UseCase
from social_oauth.infrastructure.service.google_oauth2_service import GoogleOAuth2Service
from fastapi import HTTPException

authentication_router = APIRouter()
service = GoogleOAuth2Service()
oauth_usecase = GoogleOAuth2UseCase(service)
# account_usecase = AccountUseCase(AccountRepositoryImpl())
account_usecase = AccountUseCase.getInstance()
redis_client = get_redis()

@authentication_router.get("/google")
async def redirect_to_google():
    url = oauth_usecase.get_authorization_url()
    print("[DEBUG] Redirecting to Google:", url)
    return RedirectResponse(url)


@authentication_router.get("/google/redirect")
async def process_google_redirect(
    response: Response,
    code: str,
    state: str | None = None
):
    print("[DEBUG] /google/redirect called")
    print("code:", code)
    print("state:", state)

    # code -> access token
    access_token = oauth_usecase.login_and_fetch_user(state or "", code)
    print("[DEBUG] Access token received:", access_token.access_token)
    
    # 사용자 프로필 가져오기
    user_profile = service.fetch_user_profile(access_token)
    print("[DEBUG] User profile:", user_profile)

    # 기존 유저 조회
    email = user_profile.get("email")
    existing_account = account_usecase.get_account_by_email(email)

    if not existing_account:
        # 신규 유저 - account 생성
        print("[DEBUG] New user, creating account")
        account_usecase.create_account(
            username=None,  # OAuth는 email만 사용
            email=email,
            name=user_profile.get("name", ""),
            profile_image=user_profile.get("picture"),
            provider="google",
            status="active"
        )
    else:
        # 기존 유저가 탈퇴 상태인지 확인, 테스트를 위해 임시 주석
        if existing_account.status == "deleted":
            print("[DEBUG] Account is deleted, cannot login")
            # raise HTTPException(
            #     status_code=403,
            #     detail="This account has been deleted. Please register with a new account."
            # )
        else:
            print("[DEBUG] Existing user, login only")
            # 로그인 처리 계속


    # session_id 생성
    session_id = str(uuid.uuid4())
    print("[DEBUG] Generated session_id:", session_id)

    # Redis에 session 저장 (1시간 TTL)
    redis_client.set(session_id, access_token.access_token, ex=3600)
    print("[DEBUG] Session saved in Redis:", redis_client.exists(session_id))

    # 브라우저 쿠키 발급
    redirect_response = RedirectResponse("http://localhost:3000")
    redirect_response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=3600
    )
    print("[DEBUG] Cookie set in RedirectResponse directly")
    return redirect_response

@authentication_router.get("/status")
async def auth_status(request: Request, session_id: str | None = Cookie(None)):
    print("[DEBUG] /status called")

    # 모든 요청 헤더 출력
    print("[DEBUG] Request headers:", request.headers)

    # 쿠키 확인
    print("[DEBUG] Received session_id cookie:", session_id)

    if not session_id:
        print("[DEBUG] No session_id received. Returning logged_in: False")
        return {"logged_in": False}

    exists = redis_client.exists(session_id)
    print("[DEBUG] Redis has session_id?", exists)

    return {"logged_in": bool(exists)}


@authentication_router.post("/logout")
async def logout(response: Response, session_id: str | None = Cookie(None)):
    print("[DEBUG] /logout called")
    print("[DEBUG] Session ID:", session_id)

    if session_id:
        # Redis에서 세션 삭제
        deleted = redis_client.delete(session_id)
        print(f"[DEBUG] Session deleted from Redis: {deleted}")

    # 브라우저 쿠키 삭제
    response.delete_cookie(
        key="session_id",
        httponly=True,
        secure=True,
        samesite="none"
    )
    print("[DEBUG] Cookie deleted")

    return {"message": "Logged out successfully"}
