from datetime import datetime
import requests
import os

from dotenv import load_dotenv
load_dotenv()

def fetch_today_schedule() -> str:
    try:
        today = datetime.today().strftime("%Y-%m-%d")

        base_url = os.getenv("BASE_URL", "http://54.180.31.196")
        access_token = os.getenv("ACCESS_TOKEN")
        refresh_token = os.getenv("REFRESH_TOKEN")

        response = requests.get(
            f"{base_url}/api/schedules",
            params={"date": today},
            headers={
                "Authorization": access_token,
                "Refreshtoken": refresh_token
            }
        )
        result = response.json()
        schedule_list = result.get("data", [])

        if not schedule_list:
            return "오늘은 따로 정해진 일정이 없어요~"

        formatted = "\n".join([
            f"{item['startTime'][11:16]}시에 - {item['content']}"
            for item in schedule_list
        ])
        return f"다음은 오늘의 일정입니다:\n{formatted}\n이 내용을 날짜와 시간 정보까지 포함해서 노인분께 따뜻하고 친절한 말투로 전달해줘."
    except Exception as e:
        print("일정 조회 실패:", e)
        return "일정 정보를 불러오지 못했어요."


