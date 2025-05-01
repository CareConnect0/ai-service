from fastapi.responses import JSONResponse

def success_response(data: dict, status_code: int = 200):
    return JSONResponse(
        content={
            "success": True,
            "statusCode": status_code,
            "message": "요청이 성공적으로 처리되었습니다.",
            "data": data
        },
        status_code=status_code
    )

def error_response(message: str, status_code: int = 400):
    return JSONResponse(
        content={
            "success": False,
            "statusCode": status_code,
            "message": message,
            "data": {}
        },
        status_code=status_code
    )
