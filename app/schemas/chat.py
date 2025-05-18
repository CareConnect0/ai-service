from pydantic import BaseModel

class ChatRequest(BaseModel):
    roomId: int
    user_input: str

class ChatResponse(BaseModel):
    success: bool
    status_code: int
    message: str
