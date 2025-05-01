import json
import openai
from app.core.config import settings
from typing import Tuple, List

openai.api_key = settings.openai_api_key

SYSTEM_PROMPT = """
You are an assistant whose job is to decide whether a user's message indicates an EMERGENCY situation
and to list any emergency-related keywords found in the text.
Respond in JSON **only** with two keys:
- "emergency": true or false
- "keywords": a list of extracted emergency keywords (can be empty)

Example output:
{"emergency": true, "keywords": ["도와줘", "응급"]}
"""

def detect_emergency(text: str) -> Tuple[bool, List[str]]:
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",  "content": SYSTEM_PROMPT},
            {"role": "user",    "content": text}
        ],
        temperature=0.0,
        max_tokens=60
    )
    content = resp.choices[0].message.content.strip()

    try:
        data = json.loads(content)
        is_emergency = bool(data.get("emergency", False))
        keywords     = data.get("keywords", [])
        if not isinstance(keywords, list):
            keywords = []
        return is_emergency, keywords
    except (json.JSONDecodeError, TypeError):
        return False, []
