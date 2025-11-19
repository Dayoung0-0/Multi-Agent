from pydantic import BaseModel

class UpdateBoardRequest(BaseModel):
    title: str
    content: str
    user_id: int  # 수정하는 사용자의 ID