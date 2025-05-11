import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("API_KEY")

def ask_gpt(message: str) -> str:
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 노인분들의 일정을 친절하고 따뜻하게 안내하는 ai 비서야. 일정을 부드럽게 설명해줘."},
                {"role": "user", "content": message}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print("🔥 GPT 호출 중 에러 발생:", e)
        return "⚠️ 챗봇 응답 생성 중 문제가 발생했어요. 나중에 다시 시도해주세요."
