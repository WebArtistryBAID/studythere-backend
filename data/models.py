from sqlalchemy import Column, String, Integer, DateTime

from data.database import Base


class User(Base):
    __tablename__ = 'users'
    seiueID = Column(Integer, primary_key=True, nullable=False)
    eduID = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    pinyin = Column(String(255), nullable=False)
    permissions = Column(String(1024), default="", nullable=False)
    accessToken = Column(String(1024), default="", nullable=False)
    accessTokenExpires = Column(DateTime, default=0, nullable=False)
    refreshToken = Column(String(1024), default="", nullable=False)
