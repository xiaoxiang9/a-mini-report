from sqlalchemy import text
from sqlalchemy.orm import Session


def check_database(session: Session) -> str:
    try:
        session.execute(text("SELECT 1"))
        return "up"
    except Exception:
        return "down"
