from contextlib import contextmanager
from db.database import get_session, close_session


@contextmanager
def session_scope():
    """Контекстный менеджер для работы с сессией вне FastAPI."""
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        close_session()


def with_session(func):
    """Декоратор для функций, работающих с сессией вне FastAPI."""
    def wrapper(*args, **kwargs):
        with session_scope() as session:
            return func(*args, session=session, **kwargs)
    return wrapper


def get_db():
    """Зависимость для эндпоинтов FastAPI."""
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()