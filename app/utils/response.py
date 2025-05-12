from fastapi import status
from fastapi.responses import JSONResponse
from typing import Any, Optional

def success_response(data: Any, message: str = "요청이 성공적으로 처리되었습니다.", status_code: int = status.HTTP_200_OK):
    return JSONResponse(
        content={
            "success": True,
            "statusCode": status_code,
            "message": message,
            "data": data
        },
        status_code=status_code
    )

def error_response(message: str, status_code: int = status.HTTP_400_BAD_REQUEST, data: Optional[Any] = None):
    return JSONResponse(
        content={
            "success": False,
            "statusCode": status_code,
            "message": message,
            "data": data or {}
        },
        status_code=status_code
    )
