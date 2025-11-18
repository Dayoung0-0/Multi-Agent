from typing import Optional
from sqlalchemy.orm import Session

from account.application.port.account_repository_port import AccountRepositoryPort
from account.domain.account import Account
from account.infrastructure.orm.account_orm import AccountORM
from config.database.session import get_db_session


class AccountRepositoryImpl(AccountRepositoryPort):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'db'):
            self.db: Session = get_db_session()


    def save(self, account: Account) -> Account:

        # 신규생성
        orm_account = AccountORM(
            username=account.username,
            email=account.email,
            name=account.name,
            status=account.status,
            profile_image=account.profile_image,
            provider=account.provider,
            password=account.password,
            nickname=account.nickname,
        )
        self.db.add(orm_account)

        self.db.commit()
        self.db.refresh(orm_account)

        account.id = orm_account.id
        account.created_at = orm_account.created_at
        account.updated_at = orm_account.updated_at
        return account

    def get_by_id(self, id: int) -> Optional[AccountORM]:
        return self.db.query(AccountORM).filter(AccountORM.id == id).first()

    def get_by_email(self, email: str) -> Optional[AccountORM]:
        return self.db.query(AccountORM).filter(AccountORM.email == email).first()

    def delete(self, account_id: int) -> None:
        orm_account = self.db.query(AccountORM).filter(AccountORM.id == account_id).first()
        if orm_account:
            orm_account.status = 'deleted'
            self.db.commit()

