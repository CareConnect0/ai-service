from fastapi import FastAPI
from app.routers.chatbot import router as chatbot_router

  
from dotenv import load_dotenv
import os
from app.routers import stt_schedule, stt_raw, emergency_detection
from app.routers.tts import router as tts_router

app = FastAPI()

app.include_router(chatbot_router)

@app.get("/")
def read_root():
    return {"message": "Hello, this is the chatbot API!"}

# .env 환경 변수 로드
load_dotenv()

# Google 인증 경로 확인 (선택적 로그용)
google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not google_credentials:
    print("⚠️ GOOGLE_APPLICATION_CREDENTIALS가 설정되지 않았습니다.")

# FastAPI 앱 생성
app = FastAPI(
    title="CareConnect",
    version="0.1.0",
    description="CareConnect AI API"
)

# 라우터 등록
app.include_router(stt_schedule.router, prefix="/api/ai", tags=["STT"])
app.include_router(stt_raw.router, prefix="/api/ai", tags=["STT"])
app.include_router(emergency_detection.router, prefix="/api/ai", tags=["Emergency"])
app.include_router(tts_router)

