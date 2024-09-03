from fastapi import HTTPException
from sqlalchemy.orm import Session

from data.models import User


def ensure_not_none(value):
    if value is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return value


def create_user(session: Session, user_id: str, user_seiue_id: int, user_name: str, pinyin: str | None = None, access_token: str | None = None):
    user = User(
        id=user_id,
        seiueID=user_seiue_id,
        name=user_name,
        pinyin=pinyin,
        accessToken=access_token
    )
    session.add(user)
    session.commit()
    return user


def get_user(session: Session, user_id: str):
    return session.query(User).filter(User.id == user_id).one_or_none()


def update_user(session: Session, user: User, user_name: str | None = None, pinyin: str | None = None, access_token: str | None = None):
    if user_name is not None:
        user.name = user_name
    if pinyin is not None:
        user.pinyin = pinyin
    if access_token is not None:
        user.accessToken = access_token
    session.commit()
    return user


def delete_user(session: Session, user: User):
    session.delete(user)
    session.commit()
