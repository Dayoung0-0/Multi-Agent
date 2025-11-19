from typing import List

from fastapi import APIRouter, HTTPException, Depends

from account.application.usecase.account_usecase import AccountUseCase
from account.domain.account import Account
from board.adapter.input.web.request.create_board_request import CreateBoardRequest
from board.adapter.input.web.request.update_board_request import UpdateBoardRequest
from board.adapter.input.web.response.board_response import BoardResponse
from board.application.usecase.create_board_usecase import CreateBoardUseCase
from board.application.usecase.read_board_usecase import ReadBoardUseCase
from board.application.usecase.update_board_usecase import UpdateBoardUseCase
from board.application.usecase.delete_board_usecase import DeleteBoardUseCase
from authentication.adapter.input.web.authentication_dependencies import get_current_user

board_router = APIRouter()

create_usecase = CreateBoardUseCase.getInstance()
read_usecase = ReadBoardUseCase.getInstance()
update_usecase = UpdateBoardUseCase.getInstance()
delete_usecase = DeleteBoardUseCase.getInstance()
account_usecase = AccountUseCase.getInstance()

@board_router.post("/create", response_model=BoardResponse)
def create_board(
    request: CreateBoardRequest,
    current_user: Account
    # current_user: Account = Depends(get_current_user)
):
    # 로그인한 사용자만 글 작성 가능
    # user_id는 현재 로그인한 사용자의 ID를 사용
    board = create_usecase.create_board(request.title, request.content, current_user.id)

    return BoardResponse(
        id=board.id,
        user_id=board.user_id,
        title=board.title,
        content=board.content,
        author_name=current_user.name,
        created_at=board.created_at,
        updated_at=board.updated_at,
    )

@board_router.get("/list", response_model=List[BoardResponse])
def list_boards():
    boards = read_usecase.list_boards()  # Board 정보만 가져오기

    # 각 Board에 대해 작성자 이름 가져오기
    return [
        BoardResponse(
            id=b.id,
            user_id=b.user_id,
            title=b.title,
            content=b.content,
            author_name=account_usecase.get_account(b.user_id).name if b.user_id else "Unknown",
            created_at=b.created_at,
            updated_at=b.updated_at,
        ) for b in boards
    ]

@board_router.get("/read/{board_id}", response_model=BoardResponse)
def get_board(board_id: int):
    board = read_usecase.get_by_id(board_id)
    author_name = account_usecase.get_account(board.user_id).name

    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return BoardResponse(
        id=board.id,
        user_id=board.user_id,
        title=board.title,
        author_name= author_name,
        content=board.content,
        created_at=board.created_at,
        updated_at=board.updated_at,
    )


@board_router.put("/update/{board_id}", response_model=BoardResponse)
def update_board(
    board_id: int,
    request: UpdateBoardRequest,
    current_user: Account
    # current_user: Account = Depends(get_current_user)
):
    # 게시글 조회
    existing_board = read_usecase.get_by_id(board_id)
    if not existing_board:
        raise HTTPException(status_code=404, detail="Board not found")

    # # 작성자 본인인지 확인
    # if existing_board.user_id != current_user.id:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="You don't have permission to update this board"
    #     )

    board = update_usecase.execute(
        board_id=board_id,
        title=request.title,
        content=request.content
    )

    return BoardResponse(
        id=board.id,
        user_id=board.user_id,
        title=board.title,
        content=board.content,
        author_name=current_user.name,
        created_at=board.created_at,
        updated_at=board.updated_at
    )


@board_router.delete("/delete/{board_id}")
def delete_board(
    board_id: int,
    current_user: Account,
    # current_user: Account = Depends(get_current_user)
):
    existing_board = read_usecase.get_by_id(board_id)
    if not existing_board:
        raise HTTPException(status_code=404, detail="Board not found")

    # # 작성자 본인인지 확인
    # if existing_board.user_id != current_user.id:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="You don't have permission to delete this board"
    #     )

    # 삭제 진행
    success = delete_usecase.delete_board(board_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete board")

    return {"message": "Deleted successfully"}
