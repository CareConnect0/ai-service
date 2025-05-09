from fastapi import APIRouter, File, UploadFile, HTTPException, status, Response
from app.services.stt_schedule_service import transcribe_audio
from app.utils.response import success_response, error_response

router = APIRouter()

@router.post(
    "/stt/schedule",
    summary="음성인식 (일정 추가용)",
    description="업로드한 음성 파일(wav)을 일정 추가용 텍스트로 변환합니다.",
    responses={
        200: {"description": "변환 성공"},
        400: {"description": "잘못된 파일 형식 또는 요청"},
        500: {"description": "서버 내부 오류"},
    }
)
    
async def handle_stt(
    file: UploadFile = File(...),
    response: Response = None
):
    if not file.filename.endswith((".wav", ".flac", ".mp3")):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response("지원되지 않는 파일 형식입니다.", 400)
    
    try:
        contents = await file.read()
        transcript = transcribe_audio(contents)
        return success_response(transcript, status_code=200)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return error_response("음성 인식 중 오류가 발생했습니다.", 500)


