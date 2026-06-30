from fastapi import APIRouter

from .schemas import AnonymizeRequest, AnonymizeResponse
from src.detector.ensemble_detector import detect_pii, mask_text

router = APIRouter(prefix="/api")

@router.post("/anonymize")
def anonymize(request: AnonymizeRequest):
    entities = detect_pii(request.text, request.mode)
    result = mask_text(request.text, entities)
    return AnonymizeResponse(anonymized_text=result)