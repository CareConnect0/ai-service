from pydantic import BaseModel

class ChatRequest(BaseModel):
    roomId: int
    user_input: str

class ChatResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
