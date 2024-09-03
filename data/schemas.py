from pydantic.v1 import BaseModel


class UserSchema(BaseModel):
    id: str
    name: str
    permissions: str
    pinyin: str | None

    class Config:
        from_attributes = True
