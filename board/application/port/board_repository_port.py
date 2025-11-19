from abc import ABC, abstractmethod
from typing import List, Optional

from board.domain.board import Board


class BoardRepositoryPort(ABC):

    @abstractmethod
    def save(self, board: Board) -> Board:
        pass

    @abstractmethod
    def get_by_id(self, board_id: int) -> Optional[Board]:
        pass

    @abstractmethod
    def list_all(self) -> List[Board]:
        pass

    @abstractmethod
    def update(self, board: Board) -> Board:
        pass

    @abstractmethod
    def delete(self, board_id: int) -> None:
        pass
