import os
from typing import Annotated

from fastapi import Header, Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from data.database import SessionLocal
from utils import crud

USER_AGENT = "Beijing Academy (BAID) StudyThere, Web, https://beijing.academy"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def optional_get_current_user(authorization: Annotated[str | None, Header()] = None, db: Session = Depends(get_db)):
    if authorization is None or len(authorization) == 0:
        return None
    return get_current_user(authorization, db)


def get_current_user(authorization: Annotated[str | None, Header()] = None, db: Session = Depends(get_db)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, os.environ["JWT_SECRET_KEY"], algorithms=["HS256"])
        return crud.ensure_not_none(crud.get_user(db, payload["id"]))
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
