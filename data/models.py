from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from data.database import Base


class User(Base):
    __tablename__ = 'users'
    seiueID = Column(Integer, primary_key=True, nullable=False)
    eduID = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    pinyin = Column(String(255), nullable=False)
    permissions = Column(String(1024), default='', nullable=False)
    accessToken = Column(String(1024), default='', nullable=False)
    accessTokenExpires = Column(DateTime, default=0, nullable=False)
    refreshToken = Column(String(1024), default='', nullable=False)


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(String(4), primary_key=True, nullable=False)
    description = Column(String(256))


class RoomActivity(Base):
    __tablename__ = 'roomactivities'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    roomId = Column(String(4), ForeignKey('rooms.id', ondelete='CASCADE'), nullable=False)
    room = relationship('Room', back_populates='activities')
    periodId = Column(Integer, ForeignKey('periods.id', ondelete='CASCADE'), nullable=False)
    period = relationship('Period')


# Represents a period in a day.
class Period(Base):
    __tablename__ = 'periods'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    startTime = Column(DateTime, nullable=False)  # Only time used
    endTime = Column(DateTime, nullable=False)  # Only time used
