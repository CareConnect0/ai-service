from fastapi import FastAPI
from dotenv import load_dotenv
import os

# .env 환경 변수 로드
load_dotenv()

# Google 인증 경로 확인 (선택적 로그용)
google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not google_credentials:
    print("⚠️ GOOGLE_APPLICATION_CREDENTIALS가 설정되지 않았습니다.")

# FastAPI 앱 생성
app = FastAPI()

# STT API 라우터 포함
from app.routers import stt
app.include_router(stt.router, prefix="/api/ai", tags=["STT"])
