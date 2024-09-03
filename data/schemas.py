from datetime import datetime

from pydantic.v1 import BaseModel


class UserSchema(BaseModel):
    seiueID: int
    eduID: str
    name: str
    permissions: str
    pinyin: str | None

    class Config:
        from_attributes = True


class RoomActivitySchema(BaseModel):
    id: int
    roomId: int
    periodId: int

    class Config:
        from_attributes = True


class RoomSchema(BaseModel):
    id: int
    description: str
    activities: list[RoomActivitySchema]

    class Config:
        from_attributes = True


class PeriodSchema(BaseModel):
    id: int
    startTime: datetime
    endTime: datetime
