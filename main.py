from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from app.services.tts_service import tts_stream
from app.utils.response import success_response, error_response
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

MAX_LENGTH = 500

@app.post("/api/ai/tts")
async def stream_tts(request: Request):
    data = await request.json()
    text = data.get("text", "").strip()

    # 텍스트가 없을 경우 오류 응답
    if not text:
        return error_response("텍스트가 제공되지 않았습니다", status_code=400)
    
    # 텍스트 길이가 너무 길 경우 오류 응답
    if len(text) > MAX_LENGTH:
        return error_response(f"텍스트가 너무 깁니다. (최대 {MAX_LENGTH}자)", status_code=400)

    # 성공할 경우 음성 파일만 반환(스트리밍 방식)
    return StreamingResponse(
        tts_stream(text),
        media_type="audio/mpeg"
    )
