from datetime import datetime, timezone, timedelta

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from data.schemas import RoomSchema, PeriodSchema, RoomActivityResponseSchema, \
    RoomActivityResponseType, RoomSchemaExpanded
from utils import crud
from utils.dependencies import get_db

router = APIRouter()


@router.get('/rooms', response_model=list[RoomSchema])
def get_rooms(db: Session = Depends(get_db)):
    return crud.get_rooms(db)


@router.get('/periods', response_model=list[PeriodSchema])
def get_periods(db: Session = Depends(get_db)):
    return crud.get_periods(db)


@router.get('/room', response_model=RoomSchemaExpanded)
def get_room(room: str, db: Session = Depends(get_db)):
    return crud.ensure_not_none(crud.get_room(db, room))


@router.get('/room/current', response_model=RoomActivityResponseSchema)
def get_current_activity(room: str, db: Session = Depends(get_db)):
    room_model = crud.ensure_not_none(crud.get_room(db, room))
    now = datetime.now(tz=timezone(timedelta(hours=8)))

    for activity in room_model.activities:
        start_time = datetime(now.year, now.month, now.day, int(activity.period.startTime.split(":")[0]), int(activity.period.startTime.split(":")[1]), tzinfo=timezone(timedelta(hours=8)))
        end_time = datetime(now.year, now.month, now.day, int(activity.period.endTime.split(":")[0]), int(activity.period.endTime.split(":")[1]), tzinfo=timezone(timedelta(hours=8)))
        if activity.day == now.weekday():
            if start_time.time() <= now.time() <= end_time.time():
                return RoomActivityResponseSchema(
                    type=RoomActivityResponseType.live,
                    activity=activity
                )
            # If current time is within ten minutes of start of this activity
            elif now.time() < start_time.time() and start_time.timestamp() - now.timestamp() < 600:
                return RoomActivityResponseSchema(
                    type=RoomActivityResponseType.upcoming,
                    activity=activity
                )
    return RoomActivityResponseSchema(
        type=RoomActivityResponseType.none,
        activity=None
    )
