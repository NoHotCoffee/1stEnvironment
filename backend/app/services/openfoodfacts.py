from typing import Optional

import httpx

from ..config import settings
from ..schemas import BarcodeResult, NutritionPer100g


class BarcodeLookupError(Exception):
    pass


async def lookup_barcode(barcode: str) -> Optional[BarcodeResult]:
    url = f"{settings.openfoodfacts_base_url}/product/{barcode}.json"
    headers = {"User-Agent": settings.openfoodfacts_user_agent}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
    except httpx.HTTPError as exc:
        raise BarcodeLookupError(f"Could not reach Open Food Facts: {exc}") from exc

    if response.status_code != 200:
        return None

    data = response.json()
    if data.get("status") != 1:
        return None

    product = data["product"]
    nutriments = product.get("nutriments", {})

    per_100g = NutritionPer100g(
        calories=nutriments.get("energy-kcal_100g") or 0.0,
        protein_g=nutriments.get("proteins_100g") or 0.0,
        carb_g=nutriments.get("carbohydrates_100g") or 0.0,
        fat_g=nutriments.get("fat_100g") or 0.0,
    )

    serving_size = product.get("serving_quantity")
    try:
        serving_grams = float(serving_size) if serving_size else None
    except (TypeError, ValueError):
        serving_grams = None

    name = product.get("product_name") or product.get("generic_name") or "Unknown product"

    return BarcodeResult(
        barcode=barcode,
        name=name,
        brand=product.get("brands"),
        image_url=product.get("image_front_small_url") or product.get("image_url"),
        serving_grams=serving_grams,
        per_100g=per_100g,
    )
