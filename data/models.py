from sqlalchemy import Column, String, Integer

from data.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(String(9), primary_key=True, nullable=False)
    seiueID = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    pinyin = Column(String(255), nullable=False)
    permissions = Column(String(1024), default="", nullable=False)
    accessToken = Column(String(1024), default="", nullable=False)
