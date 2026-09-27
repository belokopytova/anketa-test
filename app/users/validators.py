from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserSurveyIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    company: Optional[str] = Field(None, max_length=255)
    role: Optional[str] = Field(None, max_length=255)
    stand_interest: List[str] = Field(default_factory=list)
    directions: List[str] = Field(default_factory=list)
    interest: List[str] = Field(default_factory=list)
    phone: str = Field(..., min_length=5, max_length=50)
    email: EmailStr
    followup: Optional[str] = None


class UserSurveyOut(BaseModel):
    id: int
    message: str = "OK"

    class Config:
        from_attributes = True

class UserSurveyRead(BaseModel):
    id: int
    name: str
    company: Optional[str] = None
    role: Optional[str] = None
    stand_interest: List[str] = []
    directions: List[str] = []
    interest: List[str] = []
    phone: str
    email: EmailStr
    followup: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True