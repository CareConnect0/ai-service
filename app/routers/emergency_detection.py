from fastapi import APIRouter, File, UploadFile, Response, status
from app.services.emergency_detection_service import detect_emergency_from_text
from app.services.stt_raw_service import transcribe_audio
from app.utils.response import success_response, error_response
from app.utils.mono_converter import convert_audio_to_mono

router = APIRouter()

@router.post(
    "/emergency",
    summary="음성 파일 긴급상황 감지",
    description="업로드한 음성 파일을 텍스트로 변환한 후 긴급상황 여부와 키워드를 추출합니다.",
    responses={
        200: {"description": "변환 및 감지 성공"},
        400: {"description": "잘못된 파일 형식 또는 요청"},
        500: {"description": "서버 내부 오류"},
    }
)
async def handle_emergency(
    file: UploadFile = File(...),
    response: Response = None
):
    if not file.filename.endswith((".wav", ".flac", ".mp3")):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response("지원되지 않는 파일 형식입니다.", 400)

    try:
        contents = await file.read()

        try:
            mono_contents = convert_audio_to_mono(contents)
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return error_response(f"오디오 모노 변환 실패: {str(e)}", 400)

        transcript = transcribe_audio(mono_contents)
        if not isinstance(transcript, str):
            return transcript

        is_emergency, keywords = detect_emergency_from_text(transcript)

        result = {
            "transcript": transcript,
            "is_emergency": is_emergency,
            "keywords": keywords
        }
        return success_response(result, status_code=200)

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return error_response(f"음성 인식 및 긴급상황 감지 중 오류가 발생했습니다: {str(e)}", 500)
