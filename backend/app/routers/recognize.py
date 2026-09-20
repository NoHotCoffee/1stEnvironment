import io

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from ..config import settings
from ..deps import get_current_user
from ..models import User
from ..schemas import RecognitionResult
from ..services.classifier import ClassifierUnavailable, classify_image

router = APIRouter(prefix="/api/recognize", tags=["recognize"])


@router.post("", response_model=RecognitionResult)
async def recognize_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    contents = await file.read()
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Could not read uploaded image")

    try:
        candidates = classify_image(image, top_k=settings.food_model_top_k)
    except ClassifierUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    return RecognitionResult(
        candidates=candidates,
        default_serving_grams=settings.default_serving_grams,
    )
