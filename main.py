from fastapi import FastAPI
from pydantic import BaseModel
import openai
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("API_KEY")


app = FastAPI()

class ChatRequest(BaseModel):
    user_input: str 

class ChatResponse(BaseModel):
    success: bool
    status_code: int
    message: str

@app.get("/")
def read_root():
    return {"message": "Hello, this is the chatbot API!"}

def fetch_today_schedule() -> str:
    try:
        # today = datetime.today().strftime("%Y-%m-%d")
        # response = requests.get(
        #     "http://3.38.183.170:8080/api/schedules",
        #     params={"date": today},
        #     headers={
        #         "Authorization": "너의_ACCESS_TOKEN",
        #         "Refreshtoken": "너의_REFRESH_TOKEN"
        #     }
        # )
        #result = response.json()
        schedule_list = [
            {"startTime": "2025-05-09T09:00:00", "content": "병원 진료"},
            {"startTime": "2025-05-09T14:00:00", "content": "산책"},
            {"startTime": "2025-05-09T18:00:00", "content": "가족과 식사"}
        ]

        if not schedule_list:
            return "오늘은 따로 정해진 일정이 없어요~"

        formatted = "\n".join([
            f"{item['startTime'][11:16]}시에 - {item['content']}"
            for item in schedule_list
        ])
        return (
            f"다음은 오늘의 일정입니다:\n{formatted}\n이 내용을 날짜와 시간 정보까지 포함해서 노인분께 따뜻하고 친절한 말투로 전달해줘."
        )
    except Exception as e:
        print("❌ 일정 조회 실패:", e)
        return "⚠️ 일정 정보를 불러오지 못했어요."

def ask_gpt(message: str) -> str:
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "너는 노인분들의 일정을 친절하고 따뜻하게 안내하는 ai 비서야. 일정을 부드럽게 설명해줘."},
                {"role": "user", "content": message}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print("🔥 GPT 호출 중 에러 발생:", e)
        return "⚠️ 챗봇 응답 생성 중 문제가 발생했어요. 나중에 다시 시도해주세요."

@app.post("/api/ai/assistant", response_model=ChatResponse)
def get_bot_response(chat_request: ChatRequest):
    user_message = chat_request.user_input

    if "일정" in user_message:
        gpt_prompt = fetch_today_schedule()
    else:
        gpt_prompt = user_message

    bot_reply = ask_gpt(gpt_prompt)

    if "⚠️" in bot_reply:
        return ChatResponse(success=False, status_code=500, message=bot_reply)

    return ChatResponse(success=True, status_code=200, message=bot_reply)

@app.post("/api/assistant/request", response_model=ChatResponse)
def forward_user_message(chat_request: ChatRequest):
    user_message = chat_request.user_input
    if not user_message.strip():
        return ChatResponse(success=False, status_code=400, message="입력된 메시지가 없습니다.")

    if "일정" in user_message or "할일" in user_message:
        gpt_prompt = fetch_today_schedule()
    else:
        gpt_prompt = user_message

    bot_reply = ask_gpt(gpt_prompt)

    try:
        save_response = requests.post(
            "http://localhost:8000/api/assistant/response",
            json={
                "user_input": user_message,
                "bot_response": bot_reply,
                "user_id": 1
            }
        )
        print("✅ 응답 저장 결과:", save_response.status_code)
    except Exception as e:
        print("❌ 응답 저장 실패:", e)

    return ChatResponse(success=True, status_code=200, message=bot_reply)
