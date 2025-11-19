from board.domain.board import Board
from board.infrastructure.repository.board_repository_impl import BoardRepositoryImpl


class CreateBoardUseCase:
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

    def create_board(self, title: str, content: str, user_id: int) -> Board:
        board = Board(title=title, content=content, user_id=user_id)
        return self.board_repo.save(board)
