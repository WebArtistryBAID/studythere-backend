from pydantic.v1 import BaseModel


class UserSchema(BaseModel):
    id: str
    seiueID: int
    name: str
    permissions: str
    pinyin: str | None

    class Config:
        from_attributes = True
