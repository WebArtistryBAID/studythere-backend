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
    contributor: UserSchema

    class Config:
        from_attributes = True


class RoomSchema(BaseModel):
    id: str
    description: str
    activities: list[RoomActivitySchema]

    class Config:
        from_attributes = True


class PeriodSchema(BaseModel):
    id: int
    startTime: str
    endTime: str
