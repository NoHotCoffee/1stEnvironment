from fastapi import APIRouter, Depends, HTTPException

from ..deps import get_current_user
from ..models import User
from ..schemas import BarcodeResult
from ..services.openfoodfacts import BarcodeLookupError, lookup_barcode

router = APIRouter(prefix="/api/barcode", tags=["barcode"])


@router.get("/{barcode}", response_model=BarcodeResult)
async def get_barcode(barcode: str, current_user: User = Depends(get_current_user)):
    try:
        result = await lookup_barcode(barcode)
    except BarcodeLookupError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found in Open Food Facts")
    return result
