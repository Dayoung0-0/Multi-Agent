from typing import Optional

from board.domain.board import Board
from board.infrastructure.repository.board_repository_impl import BoardRepositoryImpl


class UpdateBoardUseCase:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.board_repo = BoardRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def execute(self, board_id: int, title: str, content: str) -> Optional[Board]:
        board = self.board_repo.get_by_id(board_id)
        if board:
            board.update(title, content)
            return self.board_repo.update(board)
        return None
