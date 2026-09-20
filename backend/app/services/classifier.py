import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Optional

from PIL import Image

from ..config import settings
from ..schemas import NutritionPer100g, RecognitionCandidate

logger = logging.getLogger(__name__)

NUTRITION_PATH = Path(__file__).resolve().parent.parent / "data" / "food101_nutrition.json"

FALLBACK_NUTRITION = NutritionPer100g(calories=200, protein_g=8, carb_g=20, fat_g=8)


@lru_cache
def _nutrition_table() -> dict:
    with open(NUTRITION_PATH) as f:
        return json.load(f)


def _lookup_nutrition(label: str) -> NutritionPer100g:
    key = label.lower().strip().replace(" ", "_").replace("-", "_")
    row = _nutrition_table().get(key)
    if row is None:
        logger.warning("No nutrition mapping for label '%s', using fallback estimate", label)
        return FALLBACK_NUTRITION
    return NutritionPer100g(**row)


class ClassifierUnavailable(Exception):
    pass


_pipeline: Optional[object] = None
_load_error: Optional[str] = None


def _get_pipeline():
    global _pipeline, _load_error
    if _pipeline is not None:
        return _pipeline
    if _load_error is not None:
        raise ClassifierUnavailable(_load_error)

    try:
        from transformers import pipeline
    except ImportError as exc:
        _load_error = f"transformers/torch not installed: {exc}"
        raise ClassifierUnavailable(_load_error) from exc

    try:
        _pipeline = pipeline("image-classification", model=settings.food_model_name)
    except Exception as exc:  # model download/offline/etc.
        _load_error = (
            f"Could not load food classification model '{settings.food_model_name}': {exc}. "
            "The model weights must be downloaded once (internet required) and are then "
            "cached locally for fully offline self-hosted use."
        )
        raise ClassifierUnavailable(_load_error) from exc

    return _pipeline


def classify_image(image: Image.Image, top_k: int = 3) -> list[RecognitionCandidate]:
    clf = _get_pipeline()
    predictions = clf(image, top_k=top_k)

    candidates = []
    for pred in predictions:
        label = pred["label"]
        confidence = float(pred["score"])
        candidates.append(
            RecognitionCandidate(
                label=label,
                confidence=confidence,
                per_100g=_lookup_nutrition(label),
            )
        )
    return candidates
