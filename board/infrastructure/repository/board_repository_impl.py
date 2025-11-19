from typing import List, Optional
from sqlalchemy.orm import Session

from board.application.port.board_repository_port import BoardRepositoryPort
from board.domain.board import Board
from board.infrastructure.orm.board_orm import BoardORM
from config.database.session import get_db_session, SessionLocal


class BoardRepositoryImpl(BoardRepositoryPort):
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

    def save(self, board: Board) -> Board:
        orm_board = BoardORM(
            user_id=board.user_id,
            title=board.title,
            content=board.content,
        )
        self.db.add(orm_board)
        self.db.commit()
        self.db.refresh(orm_board)

        board.id = orm_board.id
        board.created_at = orm_board.created_at
        board.updated_at = orm_board.updated_at
        return board

    def get_by_id(self, board_id: int) -> Optional[Board]:
        orm_board = self.db.query(BoardORM).filter(BoardORM.id == board_id).first()
        if orm_board:
            board = Board(
                title=orm_board.title,
                content=orm_board.content,
                user_id=orm_board.user_id,
            )
            board.id = orm_board.id
            board.created_at = orm_board.created_at
            board.updated_at = orm_board.updated_at
            return board
        return None

    def list_boards(self) -> List[Board]:
        orm_boards = self.db.query(BoardORM).all()
        boards = []
        for orm_board in orm_boards:
            board = Board(
                title=orm_board.title,
                content=orm_board.content,
                user_id=orm_board.user_id,
            )
            board.id = orm_board.id
            board.created_at = orm_board.created_at
            board.updated_at = orm_board.updated_at
            boards.append(board)
        return boards

    def update(self, board: Board) -> Board:
        orm_board = self.db.query(BoardORM).filter(BoardORM.id == board.id).first()
        if orm_board:
            orm_board.title = board.title
            orm_board.content = board.content
            orm_board.updated_at = board.updated_at
            self.db.commit()
            self.db.refresh(orm_board)

            board.updated_at = orm_board.updated_at
        return board

    def delete(self, board_id: int) -> None:
        self.db.query(BoardORM).filter(BoardORM.id == board_id).delete()
        self.db.commit()
