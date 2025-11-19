from board.infrastructure.repository.board_repository_impl import BoardRepositoryImpl


class DeleteBoardUseCase:
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

    def delete_board(self, board_id: int) -> bool:
        board = self.board_repo.get_by_id(board_id)
        if board:
            self.board_repo.delete(board_id)
            return True
        return False
