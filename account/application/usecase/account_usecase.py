from typing import Optional

from account.application.port.account_repository_port import AccountRepositoryPort
from account.domain.account import Account
from account.infrastructure.repository.account_repository_impl import AccountRepositoryImpl


class AccountUseCase:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.account_repo = AccountRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def create_account(
        self,
        username: Optional[str],
        email: str,
        name: str,
        profile_image: Optional[str] = None,
        provider: str = "local",
        status: str = "active",
        password: Optional[str] = None,
        nickname: Optional[str] = None
    ) -> Account:
        new_account = Account(
            username=username,
            email=email,
            name=name,
            status=status,
            profile_image=profile_image,
            provider=provider,
            password=password,
            nickname=nickname
        )
        return self.account_repo.save(new_account)

    def update_account(
        self,
        account_id: int,
        name: Optional[str] = None,
        status: Optional[str] = None,
        profile_image: Optional[str] = None
    ) -> Optional[Account]:
        account = self.account_repo.get_by_id(account_id)
        if not account:
            return None

        # domain의 update 메서드 호출
        account.update(
            name=name or account.name,
            status=status or account.status,
            profile_image=profile_image
        )
        return self.account_repo.save(account)

    def get_account(self, account_id: int) -> Optional[Account]:
        return self.account_repo.get_by_id(account_id)

    def get_account_by_email(self, email: str) -> Optional[Account]:
        return self.account_repo.get_by_email(email)

    def delete_account(self, account_id: int) -> Optional[Account]:
        account = self.account_repo.get_by_id(account_id)
        if not account:
            return None

        # domain의 update 메서드 호출
        account.update(status="deleted")
        return self.account_repo.save(account)

