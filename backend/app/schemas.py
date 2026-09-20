from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GoalsUpdate(BaseModel):
    calorie_goal: Optional[float] = None
    protein_goal_g: Optional[float] = None
    carb_goal_g: Optional[float] = None
    fat_goal_g: Optional[float] = None


class UserRead(BaseModel):
    id: int
    email: str
    calorie_goal: float
    protein_goal_g: float
    carb_goal_g: float
    fat_goal_g: float


class FoodEntryCreate(BaseModel):
    name: str
    calories: float
    protein_g: float = 0.0
    carb_g: float = 0.0
    fat_g: float = 0.0
    serving_grams: float = 100.0
    meal_type: str = "snack"
    source: str = "manual"
    barcode: Optional[str] = None
    logged_at: Optional[date] = None


class FoodEntryUpdate(BaseModel):
    name: Optional[str] = None
    calories: Optional[float] = None
    protein_g: Optional[float] = None
    carb_g: Optional[float] = None
    fat_g: Optional[float] = None
    serving_grams: Optional[float] = None
    meal_type: Optional[str] = None
    logged_at: Optional[date] = None


class FoodEntryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    calories: float
    protein_g: float
    carb_g: float
    fat_g: float
    serving_grams: float
    meal_type: str
    source: str
    barcode: Optional[str]
    logged_at: date


class DiarySummary(BaseModel):
    date: date
    entries: list[FoodEntryRead]
    total_calories: float
    total_protein_g: float
    total_carb_g: float
    total_fat_g: float
    calorie_goal: float
    protein_goal_g: float
    carb_goal_g: float
    fat_goal_g: float


class NutritionPer100g(BaseModel):
    calories: float
    protein_g: float
    carb_g: float
    fat_g: float


class BarcodeResult(BaseModel):
    barcode: str
    name: str
    brand: Optional[str] = None
    image_url: Optional[str] = None
    serving_grams: Optional[float] = None
    per_100g: NutritionPer100g
    source: str = "openfoodfacts"


class RecognitionCandidate(BaseModel):
    label: str
    confidence: float
    per_100g: NutritionPer100g


class RecognitionResult(BaseModel):
    candidates: list[RecognitionCandidate]
    default_serving_grams: float
