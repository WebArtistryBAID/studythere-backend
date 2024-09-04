from datetime import datetime
from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from data.schemas import RoomSchema, PeriodSchema, RoomActivitySchema
from utils import crud
from utils.dependencies import get_db

router = APIRouter()


@router.get('/rooms', response_model=list[RoomSchema])
def get_rooms(db: Session = Depends(get_db)):
    return crud.get_rooms(db)


@router.get('/periods', response_model=list[PeriodSchema])
def get_periods(db: Session = Depends(get_db)):
    return crud.get_periods(db)


@router.get('/room', response_model=RoomSchema)
def get_room(room: str, db: Session = Depends(get_db)):
    return crud.ensure_not_none(crud.get_room(db, room))


@router.get('/current', response_model=RoomActivitySchema | str)
def get_current_activity(room: str, db: Session = Depends(get_db)):
    room_model = crud.ensure_not_none(crud.get_room(db, room))
    now = datetime.now()
    for activity in room_model.activities:
        if activity.day == now.weekday() and activity.period.startTime <= now.time() <= activity.period.endTime:
            return activity
    return 'None'
