from fastapi import status
from typing import Any, Optional

def success_response(data: Any, message: str = "응답에 성공했습니다", status_code: int = 200):
    return {
        "success": True,
        "statusCode": status_code,
        "message": message,
        "data": data
    }

def error_response(message: str, status_code: int = 400, data: Optional[Any] = None):
    return {
        "success": False,
        "statusCode": status_code,
        "message": message,
        "data": data
    }
