from fastapi import Header
from collections.abc import Generator
from app.database.connection import SessionLocal


# def get_token(authorization: str):
#     return authorization


# def get_current_user(token: str):
#     if token is not None:
#         return {"username": "testuser"}
#     raise HTTPException(status_code=401, detail="Unauthorized")



def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()