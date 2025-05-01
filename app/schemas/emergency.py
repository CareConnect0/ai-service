from pydantic import BaseModel
from typing import List

class EmergencyRequest(BaseModel):
    text: str

class EmergencyResponse(BaseModel):
    detected: bool
    keywords: List[str]
