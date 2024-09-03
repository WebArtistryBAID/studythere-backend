from pydantic.v1 import BaseModel


class UserSchema(BaseModel):
    seiueID: int
    eduID: str
    name: str
    permissions: str
    pinyin: str | None

    class Config:
        from_attributes = True
