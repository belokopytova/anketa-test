from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.users.validators import UserSurveyIn, UserSurveyOut, UserSurveyRead
from app.users.services import save_survey, get_all_surveys, find_duplicate
from db.session import get_db

router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/save", response_model=UserSurveyOut)
def save_user_survey(payload: UserSurveyIn, db: Session = Depends(get_db)):

    existing, reason = find_duplicate(db, payload.phone, payload.email)

    if existing:
        if reason == "phone+email":
            msg = "Анкета с таким телефоном и email уже есть."
        elif reason == "phone":
            msg = "Анкета с таким телефоном уже есть."
        else:
            msg = "Анкета с таким email уже есть."

        raise HTTPException(status_code=409, detail=msg)

    try:
        user = save_survey(db, payload)
        return UserSurveyOut(id=user.id, message="Анкета сохранена")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения: {e}")


@router.get("/all", response_model=List[UserSurveyRead])
def list_surveys(db: Session = Depends(get_db)):
    """Все анкеты в JSON."""
    return get_all_surveys(db)


@router.get("/{survey_id}", response_model=UserSurveyRead)
def get_survey(survey_id: int, db: Session = Depends(get_db)):
    """Одна анкета по ID."""
    from app.users.models import UserSurvey
    obj = db.query(UserSurvey).filter(UserSurvey.id == survey_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Анкета не найдена")
    return obj