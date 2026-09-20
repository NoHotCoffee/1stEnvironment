from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    calorie_goal: float = 2000.0
    protein_goal_g: float = 100.0
    carb_goal_g: float = 250.0
    fat_goal_g: float = 65.0


class FoodEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")

    name: str
    calories: float
    protein_g: float = 0.0
    carb_g: float = 0.0
    fat_g: float = 0.0

    serving_grams: float = 100.0
    meal_type: str = "snack"  # breakfast | lunch | dinner | snack
    source: str = "manual"  # manual | barcode | photo
    barcode: Optional[str] = None

    logged_at: date = Field(default_factory=date.today, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
