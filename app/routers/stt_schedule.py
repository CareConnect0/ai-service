from fastapi import APIRouter, File, UploadFile, HTTPException, status, Response
from app.services.stt_schedule_service import transcribe_audio
from app.utils.response import success_response, error_response
from app.utils.mono_converter import convert_audio_to_mono
import traceback

router = APIRouter()

# 최대 파일 크기 제한 (5MB)
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024  # 바이트 단위

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

        # 파일 크기 체크 (5MB 초과 시 예외)
        if len(contents) > MAX_FILE_SIZE:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return error_response(f"파일 크기가 {MAX_FILE_SIZE_MB}MB를 초과했습니다.", 400)
        
        # 스테레오 → 모노 변환
        mono_contents = convert_audio_to_mono(contents)

        transcript = transcribe_audio(mono_contents)
        
        return success_response(transcript, status_code=200)
    except Exception as e:
        # 예외 메시지 출력
        print("STT 처리 중 예외 발생:", str(e))
        traceback.print_exc()  # 전체 에러 스택 출력
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return error_response("음성 인식 중 오류가 발생했습니다.", 500)


