from fastapi import APIRouter, Depends
from app.schemas.emergency import EmergencyRequest, EmergencyResponse
from app.services.detector import detect_emergency
from app.auth.jwt_handler import verify_token

router = APIRouter(
    prefix="/api/ai/emergency-detect",
    tags=["Emergency"]
)

@router.post(
    "",
    response_model=EmergencyResponse,
    # dependencies=[Depends(verify_token)]
)
async def emergency_detect(request: EmergencyRequest):
    detected, keywords = detect_emergency(request.text)
    return EmergencyResponse(detected=detected, keywords=keywords)
