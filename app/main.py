from fastapi import FastAPI
from app.routers.chatbot import router as chatbot_router

app = FastAPI()

app.include_router(chatbot_router)

@app.get("/")
def read_root():
    return {"message": "Hello, this is the chatbot API!"}