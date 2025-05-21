import os
import json
from openai import OpenAI
from typing import Tuple, List

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an emergency‐detection assistant. The input message will be in Korean.
Your tasks:
1. Determine if the text describes a life‐threatening or serious emergency requiring immediate assistance.
2. Extract and return any emergency‐related keywords.
Output must be valid JSON **only** with two keys:
- "emergency": true or false
- "keywords": a list of strings (can be empty)

Do not include any extra fields or commentary.
"""

FEW_SHOT_EXAMPLES = [
    {
        "user":      "화재가 났어요. 빨리 도와주세요!",
        "assistant": {"emergency": True,  "keywords": ["화재", "도와주세요"]}
    },
    {
        "user":      "심장마비가 온 것 같아요. 119 불러주세요!",
        "assistant": {"emergency": True,  "keywords": ["심장마비", "119"]}
    },
    {
        "user":      "오늘 날씨가 정말 좋네요.",
        "assistant": {"emergency": False, "keywords": []}
    },
    {
        "user":      "배고파요. 점심 뭐 먹을까요?",
        "assistant": {"emergency": False, "keywords": []}
    },
    {
        "user":      "미끄러졌어. 다리가 아파서 못 일어나겠어요.",
        "assistant": {"emergency": True,  "keywords": ["미끄러졌어", "다리", "못 일어나겠어요"]}
    },
]

def detect_emergency_from_text(text: str) -> Tuple[bool, List[str]]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for ex in FEW_SHOT_EXAMPLES:
        messages.append({"role": "user",      "content": ex["user"]})
        messages.append({
            "role": "assistant",
            "content": json.dumps(ex["assistant"], ensure_ascii=False)
        })
    messages.append({"role": "user", "content": text})

    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.0,
        max_tokens=80
    )
    content = resp.choices[0].message.content.strip()

    try:
        data = json.loads(content)
        is_emergency = bool(data.get("emergency", False))
        keywords = data.get("keywords", [])
        if not isinstance(keywords, list):
            keywords = []
        return is_emergency, keywords

    except (json.JSONDecodeError, TypeError):
        return False, []
    except Exception as e:
        print(f"[EmergencyDetectionError] {e}")
        return False, []
