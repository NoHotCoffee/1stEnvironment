from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..deps import get_current_user
from ..models import FoodEntry, User
from ..schemas import DiarySummary, FoodEntryCreate, FoodEntryRead, FoodEntryUpdate

router = APIRouter(prefix="/api/diary", tags=["diary"])


@router.post("", response_model=FoodEntryRead)
def create_entry(
    payload: FoodEntryCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    entry = FoodEntry(
        user_id=current_user.id,
        logged_at=payload.logged_at or date.today(),
        **payload.model_dump(exclude={"logged_at"}),
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


@router.get("", response_model=DiarySummary)
def get_diary(
    for_date: date = date.today(),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    entries = session.exec(
        select(FoodEntry)
        .where(FoodEntry.user_id == current_user.id)
        .where(FoodEntry.logged_at == for_date)
        .order_by(FoodEntry.created_at)
    ).all()

    return DiarySummary(
        date=for_date,
        entries=entries,
        total_calories=sum(e.calories for e in entries),
        total_protein_g=sum(e.protein_g for e in entries),
        total_carb_g=sum(e.carb_g for e in entries),
        total_fat_g=sum(e.fat_g for e in entries),
        calorie_goal=current_user.calorie_goal,
        protein_goal_g=current_user.protein_goal_g,
        carb_goal_g=current_user.carb_goal_g,
        fat_goal_g=current_user.fat_goal_g,
    )


def _get_owned_entry(entry_id: int, current_user: User, session: Session) -> FoodEntry:
    entry = session.get(FoodEntry, entry_id)
    if not entry or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.put("/{entry_id}", response_model=FoodEntryRead)
def update_entry(
    entry_id: int,
    payload: FoodEntryUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    entry = _get_owned_entry(entry_id, current_user, session)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


@router.delete("/{entry_id}")
def delete_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    entry = _get_owned_entry(entry_id, current_user, session)
    session.delete(entry)
    session.commit()
    return {"ok": True}
