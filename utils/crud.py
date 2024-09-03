from datetime import datetime, timedelta

import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from data.models import User
from utils.dependencies import USER_AGENT


def ensure_not_none(value):
    if value is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return value


def create_user(session: Session, user_seiue_id: int, user_edu_id: str, user_name: str, pinyin: str, access_token: str,
                access_token_expires: datetime, refresh_token: str):
    user = User(
        seiueID=user_seiue_id,
        eduID=user_edu_id,
        name=user_name,
        pinyin=pinyin,
        accessToken=access_token,
        accessTokenExpires=access_token_expires,
        refreshToken=refresh_token
    )
    session.add(user)
    session.commit()
    return user


def get_user(session: Session, user_id: str):
    return session.query(User).filter(User.seiueID == user_id).one_or_none()


def update_user(session: Session, user: User, user_name: str | None = None, pinyin: str | None = None,
                access_token: str | None = None, access_token_expires: datetime | None = None,
                refresh_token: str | None = None):
    if user_name is not None:
        user.name = user_name
    if pinyin is not None:
        user.pinyin = pinyin
    if access_token is not None:
        user.accessToken = access_token
    if access_token_expires is not None:
        user.accessTokenExpires = access_token_expires
    if refresh_token is not None:
        user.refreshToken = refresh_token
    session.commit()
    return user


def delete_user(session: Session, user: User):
    session.delete(user)
    session.commit()


def update_schedules_based_on_user(session: Session, user: User):
    # Get events from beginning of this calendar week to end of this calendar week
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    r = requests.get(f" https://api.seiue.com/chalk/calendar/personals/{user.seiueID}/events",
                     params={
                         "expand": "address,initiators",
                         "start_time": f"{monday.year}-{str(monday.month).zfill(2)}-{str(monday.day).zfill(2)} 00:00:00",
                         "end_time": f"{sunday.year}-{str(sunday.month).zfill(2)}-{str(sunday.day).zfill(2)} 23:59:59"
                     },
                     headers={
                         "Authorization": f"Bearer {user.accessToken}",
                         "X-School-Id": "452",
                         "User-Agent": USER_AGENT
                     })
    print(r.text)
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="SEIUE request for events failed")
