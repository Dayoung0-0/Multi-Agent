from fastapi import APIRouter, HTTPException

from account.adapter.input.web.request.create_account_request import CreateAccountRequest
from account.adapter.input.web.request.update_account_request import UpdateAccountRequest
from account.adapter.input.web.response.account_response import AccountResponse
from account.application.usecase.account_usecase import AccountUseCase
from account.infrastructure.repository.account_repository_impl import AccountRepositoryImpl

account_router = APIRouter()
usecase = AccountUseCase.getInstance()

@account_router.post("/create", response_model=AccountResponse)
def create_account(request: CreateAccountRequest):
    account = usecase.create_account(
        username=request.username,
        email=request.email,
        name=request.name,
        profile_image=request.profile_image,
        provider=request.provider,
        status=request.status,
        password=request.password,
        nickname=request.nickname
    )
    return AccountResponse(
        id=account.id,
        email=account.email,
        name=account.name,
        profile_image=account.profile_image,
        provider=account.provider,
        created_at=account.created_at,
        updated_at=account.updated_at,
    )


@account_router.put("/update/{account_id}", response_model=AccountResponse)
def update_account(account_id: int, request: UpdateAccountRequest):
    account = usecase.update_account(
        account_id=account_id,
        name=request.name,
        status=request.status,
        profile_image=request.profile_image
    )
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountResponse(
        id=account.id,
        email=account.email,
        name=account.name,
        profile_image=account.profile_image,
        provider=account.provider,
        created_at=account.created_at,
        updated_at=account.updated_at,
    )


@account_router.get("/get/id/{account_id}", response_model=AccountResponse)
def get_account(account_id: int):
    account = usecase.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountResponse(
        id=account.id,
        email=account.email,
        name=account.name,
        profile_image=account.profile_image,
        provider=account.provider,
        created_at=account.created_at,
        updated_at=account.updated_at,
    )


@account_router.get("/get/email/{email}", response_model=AccountResponse)
def get_account_by_email(email: str):
    account = usecase.get_account_by_email(email)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountResponse(
        id=account.id,
        email=account.email,
        name=account.name,
        profile_image=account.profile_image,
        provider=account.provider,
        created_at=account.created_at,
        updated_at=account.updated_at,
    )


@account_router.delete("/delete/{account_id}")
def delete_account(account_id: int):
    usecase.delete_account(account_id)
    return {"message": "Deleted successfully"}
