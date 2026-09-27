import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///instance/users.db",
    )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    SQLALCHEMY_ECHO = os.getenv(
        "SQLALCHEMY_ECHO",
        "False",
    ).lower() == "true"

    DEBUG = os.getenv(
        "DEBUG",
        "False",
    ).lower() == "true"
