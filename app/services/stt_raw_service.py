from google.cloud import speech
from openai import OpenAI
import os
from app.utils.response import error_response

# OpenAI API 키 로드
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def transcribe_audio(file_bytes: bytes) -> str:
    try:
        # Google STT 클라이언트 설정
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(content=file_bytes)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            # sample_rate_hertz=16000,
            language_code="ko-KR"
        )

        response = client.recognize(config=config, audio=audio)

        if not response.results:
            return error_response("음성을 인식할 수 없습니다.", 400)

        # 텍스트 가져오기
        transcript = " ".join([result.alternatives[0].transcript for result in response.results])

        return transcript

    except Exception as e:
        return error_response(f"음성 인식 중 오류가 발생했습니다: {str(e)}", 500)
