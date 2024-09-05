from datetime import datetime, timedelta

import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from data.models import User, Period, RoomActivity, Room
from utils.dependencies import USER_AGENT


def ensure_not_none(value):
    if value is None:
        raise HTTPException(status_code=404, detail='Not Found')
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


def get_rooms(session: Session):
    return session.query(Room).all()


def get_periods(session: Session):
    return session.query(Period).all()


def get_room(session: Session, room_id: str):
    return session.query(Room).filter(Room.id == room_id).one_or_none()


def get_period(session: Session, period_time: str):
    return session.query(Period).filter(Period.startTime == period_time).one_or_none()


def get_room_activity(session: Session, period_id: int, day: int, room_id: str, name: str):
    return session.query(RoomActivity).filter(RoomActivity.periodId == period_id, RoomActivity.day == day,
                                              RoomActivity.roomId == room_id, RoomActivity.name == name).one_or_none()


def update_schedules_based_on_user(session: Session, user: User):
    # Get events from beginning of this calendar week to end of this calendar week
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    r = requests.get(f' https://api.seiue.com/chalk/calendar/personals/{user.seiueID}/events',
                     params={
                         'expand': 'address,initiators',
                         'start_time': f'{monday.year}-{str(monday.month).zfill(2)}-{str(monday.day).zfill(2)} 00:00:00',
                         'end_time': f'{sunday.year}-{str(sunday.month).zfill(2)}-{str(sunday.day).zfill(2)} 23:59:59'
                     },
                     headers={
                         'Authorization': f'Bearer {user.accessToken}',
                         'X-School-Id': '452',
                         'User-Agent': USER_AGENT
                     })
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail='SEIUE request for events failed')
    data = r.json()
    for clazz in data:
        start_time = datetime.strptime(clazz['start_time'], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(clazz['end_time'], '%Y-%m-%d %H:%M:%S')
        period = get_period(session, start_time.strftime('%H:%M'))
        if period is None:
            period = Period(startTime=start_time.strftime('%H:%M'), endTime=end_time.strftime('%H:%M'))
            session.add(period)
            session.commit()
        name = clazz['title']
        if '体育' in name or '自习' in name:
            continue
        room = clazz['address'].replace('机房', '')
        people = ''

        room_model = get_room(session, room)
        if room_model is None:
            room_model = Room(id=room, description='')
            session.add(room_model)
            session.commit()

        activity = get_room_activity(session, period.id, start_time.weekday(), room, name)
        if activity is None:
            activity = RoomActivity(name=name, day=start_time.weekday(), people=people, periodId=period.id, contributorId=user.seiueID)
            activity.room = room_model
            session.add(activity)
            session.commit()
