from fastapi import APIRouter, File, UploadFile, HTTPException, status, Response
from app.services.stt_schedule_service import transcribe_audio
from app.utils.response import success_response, error_response

router = APIRouter()

@router.post("/stt/schedule")
async def handle_stt(file: UploadFile = File(...), response: Response = None):
    if not file.filename.endswith((".wav", ".flac", ".mp3")):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response("지원되지 않는 파일 형식입니다.", 400)
    
    contents = await file.read()
    transcript = transcribe_audio(contents)  # 음성 파일을 텍스트로 변환하고 형식 변경

    return success_response(transcript, status_code=200)


