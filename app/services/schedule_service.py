from datetime import datetime
import requests

def fetch_today_schedule() -> str:
    try:
        # 실제 api 호출할때 코드!
        # today = datetime.today().strftime("%Y-%m-%d")
        # response = requests.get(
        #     "http://3.38.183.170:8080/api/schedules",
        #     params={"date": today},
        #     headers={
        #         "Authorization": "ACCESS_TOKEN",
        #         "Refreshtoken": "REFRESH_TOKEN"
        #     }
        # )
        #result = response.json()
    
        schedule_list = [
            {"startTime": "2025-05-09T09:00:00", "content": "병원 진료"},
            {"startTime": "2025-05-09T14:00:00", "content": "산책"},
            {"startTime": "2025-05-09T18:00:00", "content": "가족과 식사"}
        ]

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
