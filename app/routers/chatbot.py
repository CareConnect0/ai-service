from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.gpt_service import ask_gpt
from app.services.schedule_service import fetch_today_schedule
import requests
import os

router = APIRouter()

BASE_URL = os.getenv("BASE_URL", "http://3.38.183.170:8080")
HEADERS = {
    "Authorization": os.getenv("ACCESS_TOKEN", "임시_ACCESS_TOKEN"),
    "Refreshtoken": os.getenv("REFRESH_TOKEN", "임시_REFRESH_TOKEN")

}

@router.post("/api/ai/assistant", response_model=ChatResponse)
def get_bot_response(chat_request: ChatRequest):
    user_message = chat_request.user_input
    gpt_prompt = fetch_today_schedule() if "일정" in user_message or "할일" in user_message else user_message
    bot_reply = ask_gpt(gpt_prompt)

    if "⚠️" in bot_reply:
        return ChatResponse(success=False, status_code=500, message=bot_reply)
    
    try:
        response1 = requests.post(
            f"{BASE_URL}/api/assistant/request",
            headers=HEADERS,
            json={
                "roomId": 1, 
                "requestMessage": user_message
            }
        )
        print(" 사용자 메시지 저장:", response1.status_code)
    except Exception as e:
        print(" 사용자 메시지 저장 실패:", e)
        
    try:
        response2 = requests.post(
            f"{BASE_URL}/api/assistant/response",
            headers=HEADERS,
            json={
                "roomId": 1,  
                "responseMessage": bot_reply
            }
        )
        print("GPT 응답 저장:", response2.status_code)
    except Exception as e:
        print("GPT 응답 저장 실패:", e)

    return ChatResponse(success=True, status_code=200, message=bot_reply)
