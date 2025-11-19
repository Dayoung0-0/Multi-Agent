from typing import List, Optional

from board.domain.board import Board
from board.infrastructure.repository.board_repository_impl import BoardRepositoryImpl


class ReadBoardUseCase:
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

    def get_by_id(self, board_id: int) -> Optional[Board]:
        return self.board_repo.get_by_id(board_id)

    # def list_boards(self) -> List[Board]:
    #     return self.board_repo.list_all()

    def list_boards(self) -> List[BoardResponse]:
        boards = self.board_repo.list_boards()
        responses = []

        for board in boards:
            # 작성자 정보 가져오기
            account = self.account_repo.get_by_id(board.user_id)
            author_name = account.name if account else "Unknown"

            responses.append(
                BoardResponse(
                    id=board.id,
                    author_id=board.user_id,
                    title=board.title,
                    content=board.content,
                    author_name=author_name,
                    created_at=board.created_at,
                    updated_at=board.updated_at,
                )
            )
