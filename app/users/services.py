from sqlalchemy.orm import Session
from app.users.models import UserSurvey


def save_survey(db: Session, data) -> UserSurvey:
    obj = UserSurvey(
        name=data.name,
        company=data.company,
        role=data.role,
        stand_interest=data.stand_interest,
        directions=data.directions,
        interest=data.interest,
        phone=data.phone,
        email=data.email,
        followup=data.followup,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_all_surveys(db: Session):

    return (
        db.query(UserSurvey)
        .order_by(UserSurvey.created_at.desc())
        .all()
    )

def find_duplicate(db: Session, phone: str, email: str):

    phone = (phone or "").strip()
    email = (email or "").strip().lower()

    by_phone = (
        db.query(UserSurvey)
        .filter(UserSurvey.phone == phone)
        .first()
    )
    by_email = (
        db.query(UserSurvey)
        .filter(UserSurvey.email == email)
        .first()
    )

    if by_phone and by_email:
        return by_phone, "phone+email"
    if by_phone:
        return by_phone, "phone"
    if by_email:
        return by_email, "email"
    return None, None