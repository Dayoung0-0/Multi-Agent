from abc import ABC, abstractmethod
from typing import Optional

from account.domain.account import Account


class AccountRepositoryPort(ABC):

    @abstractmethod
    def save(self, account: Account) -> Account:
        pass

    @abstractmethod
    def get_by_id(self, account_id: int) -> Optional[Account]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Account]:
        pass

    @abstractmethod
    def delete(self, account_id: int) -> Optional[Account]:
        pass
