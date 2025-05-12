from fastapi import FastAPI
from app.routers.tts import router as tts_router

# FastAPI 앱 생성
app = FastAPI(
    title="CareConnect",
    version="0.1.0",
    description="CareConnect AI API"
)

app.include_router(tts_router)
