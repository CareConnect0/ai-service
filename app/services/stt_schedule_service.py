from google.cloud import speech
from openai import OpenAI
import os
from app.utils.response import error_response
import traceback

# OpenAI API 키 로드
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def transcribe_audio(file_bytes: bytes) -> str:
    try:
        # Google STT 클라이언트 설정
        client = speech.SpeechClient()

        audio = speech.RecognitionAudio(content=file_bytes)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="ko-KR",
            enable_automatic_punctuation=True
        )

        # 비동기 방식으로 요청
        operation = client.long_running_recognize(config=config, audio=audio)

        # 최대 300초 대기 (길이에 따라 조정 가능)
        response = operation.result(timeout=300)

        if not response.results:
            return error_response("음성을 인식할 수 없습니다.", 400)

        transcript = " ".join([result.alternatives[0].transcript for result in response.results])

        formatted_transcript = format_schedule_text(transcript)

        return formatted_transcript

    except Exception as e:
        print("Google STT 처리 오류:", str(e))
        traceback.print_exc()
        return error_response(f"음성 인식 중 오류가 발생했습니다: {str(e)}", 500)

def format_schedule_text(input_text: str) -> str:
    prompt = f"당신은 사용자의 말을 듣고, 일정 항목으로 정리하는 비서입니다. 구어체, 감정 표현, 불필요한 말은 제거하고, 핵심 일정만 '~하기' 형식으로 요약하세요(날짜, 시간 제외하고 출력에 기호 제외하기).\n{input_text}"

    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=100,
            temperature=0.7,
        )

        formatted_text = completion.choices[0].message.content
        return formatted_text

    except Exception as e:
        return error_response(f"일정 내용 변환 중 오류가 발생했습니다: {str(e)}", 500)
