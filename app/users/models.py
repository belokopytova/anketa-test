from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from db.database import Base


class UserSurvey(Base):
    __tablename__ = "user_surveys"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    role = Column(String(255), nullable=True)
    stand_interest = Column(JSON, default=list)
    directions = Column(JSON, default=list)
    interest = Column(JSON, default=list)
    phone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    followup = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)