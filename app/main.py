from fastapi import FastAPI
from app.routers.emergency import router as emergency_router

app = FastAPI(
    title="CareConnect",
    version="0.1.0",
    description="노인 긴급 단어 감지"
)

app.include_router(emergency_router)
