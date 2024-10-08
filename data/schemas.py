import enum

from pydantic import BaseModel


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
    name: str
    day: int
    people: str
    roomId: str
    periodId: int
    contributor: UserSchema | None

    class Config:
        from_attributes = True


class RoomActivityResponseType(enum.Enum):
    none = 'none'
    live = 'live'
    upcoming = 'upcoming'


class RoomActivityResponseSchema(BaseModel):
    type: RoomActivityResponseType
    activity: RoomActivitySchema | None


class RoomSchema(BaseModel):
    id: str
    description: str

    class Config:
        from_attributes = True


class RoomSchemaExpanded(RoomSchema):
    activities: list[RoomActivitySchema]

    class Config:
        from_attributes = True


class PeriodSchema(BaseModel):
    id: int
    startTime: str
    endTime: str
