from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.gpt_service import ask_gpt
from app.services.schedule_service import fetch_today_schedule
import requests

router = APIRouter()

@router.post("/api/ai/assistant", response_model=ChatResponse)
def get_bot_response(chat_request: ChatRequest):
    user_message = chat_request.user_input
    gpt_prompt = fetch_today_schedule() if "일정" in user_message else user_message
    bot_reply = ask_gpt(gpt_prompt)

    if "⚠️" in bot_reply:
        return ChatResponse(success=False, status_code=500, message=bot_reply)
    return ChatResponse(success=True, status_code=200, message=bot_reply)

@router.post("/api/assistant/request", response_model=ChatResponse)
def forward_user_message(chat_request: ChatRequest):
    user_message = chat_request.user_input
    if not user_message.strip():
        return ChatResponse(success=False, status_code=400, message="입력된 메시지가 없습니다.")
    
    gpt_prompt = fetch_today_schedule() if "일정" in user_message or "할일" in user_message else user_message
    bot_reply = ask_gpt(gpt_prompt)

    try:
        save_response = requests.post(
            "http://localhost:8000/api/assistant/response",
            json={"user_input": user_message, "bot_response": bot_reply, "user_id": 1}
        )
        print("응답 저장 결과:", save_response.status_code)
    except Exception as e:
        print("응답 저장 실패:", e)

    return ChatResponse(success=True, status_code=200, message=bot_reply)
