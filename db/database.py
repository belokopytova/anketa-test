from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

from config import Config   

DATABASE_URL = Config.DATABASE_URL

connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    DATABASE_URL,
    echo=Config.SQLALCHEMY_ECHO,
    connect_args=connect_args,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
_scoped = scoped_session(SessionLocal)

Base = declarative_base()


def get_session():
    return _scoped()


def close_session():
    _scoped.remove()


def get_engine():
    return engine


def init_db(app=None):

    """Создать все таблицы"""

    from app.users import models  

    import os
    from pathlib import Path
    if DATABASE_URL.startswith("sqlite:///"):
        db_path = DATABASE_URL.replace("sqlite:///", "", 1)
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    Base.metadata.create_all(bind=engine)