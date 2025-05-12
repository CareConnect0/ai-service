from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.services.tts_service import tts_stream
from app.utils.response import error_response
from pydantic import BaseModel

router = APIRouter()

MAX_LENGTH = 500

class TTSRequest(BaseModel):
    text: str

@router.post(
    "/api/ai/tts",
    response_class=StreamingResponse,
    tags=["TTS"],
    summary="텍스트를 음성으로 변환",
    description="입력된 텍스트를 TTS로 변환하여 오디오(MP3)를 스트리밍합니다.",
    responses={
        200: {"description": "성공적으로 MP3 스트리밍 시작"},
        400: {"description": "요청 오류 (텍스트 없음 또는 길이 초과)"}
    }
)

async def stream_tts(body: TTSRequest):
    text = body.text.strip()

    if not text:
        return error_response("텍스트가 제공되지 않았습니다", status_code=400)

    if len(text) > MAX_LENGTH:
        return error_response(f"텍스트가 너무 깁니다. (최대 {MAX_LENGTH}자)", status_code=400)

    return StreamingResponse(
        tts_stream(text),
        media_type="audio/mpeg"
    )
